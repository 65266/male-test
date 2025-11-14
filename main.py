from simulation import GenderRatioSimulation
import analysis


def get_experiment_parameters():
    """获取用户输入的实验参数"""
    print("=== 请输入实验参数 ===")

    # 初始夫妻数量
    while True:
        try:
            initial_couples = int(input("请输入初始夫妻数量（正整数）: "))
            if initial_couples > 0:
                break
            print("错误：请输入大于0的正整数！")
        except ValueError:
            print("错误：请输入有效的数字！")

    # 最大生育数量
    while True:
        try:
            max_children = int(input("请输入每个家庭最大生育数量（正整数）: "))
            if max_children > 0:
                break
            print("错误：请输入大于0的正整数！")
        except ValueError:
            print("错误：请输入有效的数字！")

    # 模拟次数
    while True:
        try:
            simulation_runs = int(input("请输入模拟实验次数（正整数）: "))
            if simulation_runs > 0:
                break
            print("错误：请输入大于0的正整数！")
        except ValueError:
            print("错误：请输入有效的数字！")

    # 生育策略选择
    print("\n=== 请选择生育策略 ===")
    print("1. 生到男孩为止")
    print("2. 生到2个男孩为止")
    print("3. 固定生育数量")

    while True:
        try:
            strategy_choice = int(input("请选择策略（1-3）: "))
            if 1 <= strategy_choice <= 3:
                break
            print("错误：请选择1-3之间的数字！")
        except ValueError:
            print("错误：请输入有效的数字！")

    # 根据策略获取额外参数
    strategy_params = {}
    if strategy_choice == 1:
        strategy_params['type'] = 'stop_at_boy'
        strategy_name = "生到男孩为止"
    elif strategy_choice == 2:
        strategy_params['type'] = 'stop_at_two_boys'
        strategy_name = "生到2个男孩为止"
    else:  # 策略3：固定生育数量
        while True:
            try:
                fixed_num = int(input("请输入固定生育数量（正整数）: "))
                if fixed_num > 0 and fixed_num <= max_children:
                    break
                print(f"错误：请输入1-{max_children}之间的正整数！")
            except ValueError:
                print("错误：请输入有效的数字！")
        strategy_params['type'] = 'fixed_children'
        strategy_params['number'] = fixed_num
        strategy_name = f"固定生育{fixed_num}个孩子"

    # 显示选择的策略
    print(f"\n已选择生育策略：{strategy_name}")

    return {
        'initial_couples': initial_couples,
        'max_children': max_children,
        'simulation_runs': simulation_runs,
        'strategy': strategy_params
    }


def print_round_results(results):
    """打印每一轮的具体结果"""
    if not results:
        print("没有模拟结果可显示")
        return

    # 打印表头
    print("\n" + "=" * 80)
    print("每一轮模拟具体结果：")
    print("-" * 80)
    print(f"{'轮次':<6} {'男孩总数':<10} {'女孩总数':<10} {'总孩子数':<10} {'男孩比例':<12} {'平均家庭规模':<15}")
    print("-" * 80)

    # 打印每轮数据
    for round_data in results:
        print(
            f"{round_data['run']:<6} "
            f"{round_data['total_boys']:<10} "
            f"{round_data['total_girls']:<10} "
            f"{round_data['total_children']:<10} "
            f"{round_data['boy_ratio']:.4f}        "  # 男孩比例保留4位小数
            f"{round_data['avg_family_size']:.2f}"  # 平均家庭规模保留2位小数
        )

    print("-" * 80 + "\n")


if __name__ == "__main__":
    # 1. 获取用户输入的实验参数
    params = get_experiment_parameters()

    # 2. 确认参数
    print("\n=== 实验参数确认 ===")
    print(f"初始夫妻数量：{params['initial_couples']}")
    print(f"每个家庭最大生育数量：{params['max_children']}")
    print(f"模拟实验次数：{params['simulation_runs']}")
    print(f"生育策略：{params['strategy']['type']}")
    if params['strategy']['type'] == 'fixed_children':
        print(f"固定生育数量：{params['strategy']['number']}")

    # 3. 创建模拟对象
    try:
        sim = GenderRatioSimulation(
            initial_couples=params['initial_couples'],
            max_children=params['max_children'],
            strategy=params['strategy']
        )
    except ValueError as e:
        print(f"\n创建模拟对象失败：{e}")
        exit(1)

    # 4. 运行模拟
    print("\n=== 开始模拟实验 ===")
    try:
        results = sim.run(runs=params['simulation_runs'])
    except Exception as e:
        print(f"模拟过程出错：{e}")
        exit(1)

    # 5. 打印每一轮具体结果（新增部分）
    print_round_results(results)

    # 6. 分析结果
    print("\n=== 分析模拟结果 ===")
    stats_summary = analysis.analyze_results(results)
    if not stats_summary:
        print("分析结果为空，可能模拟未产生有效数据")
        exit(1)

    # 7. 打印统计摘要
    analysis.print_summary(stats_summary)

    # 8. 绘制结果图表
    print("\n=== 生成结果图表 ===")
    try:
        analysis.plot_results(results, stats_summary)
    except Exception as e:
        print(f"绘制图表出错：{e}")

    print("\n=== 实验完成 ===")