from simulation import GenderRatioSimulation
from analysis import analyze_results, plot_results, print_summary


def main():
    print("开始性别比例模拟实验...")

    # 实验参数设置
    initial_couples = 10000  # 初始夫妻数量
    max_children = None  # 最大生育数量（None表示无限制）
    num_simulations = 50  # 模拟次数

    print(f"实验参数: 初始夫妻={initial_couples}, 最大生育数={max_children}, 模拟次数={num_simulations}")

    # 创建实验实例
    experiment = GenderRatioSimulation(initial_couples=initial_couples, max_children=max_children)

    # 运行模拟
    results = experiment.run_simulation(num_simulations=num_simulations)

    # 分析结果
    stats_summary = analyze_results(results)

    # 打印统计摘要
    print_summary(stats_summary)

    # 绘制图表
    plot_results(results, stats_summary)

    print("\n实验完成！")


if __name__ == "__main__":
    main()
