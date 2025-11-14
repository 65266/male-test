import random
import numpy as np


class GenderRatioSimulation:
    """
    性别比例模拟类

    支持三种生育策略：
    1. 生到男孩为止
    2. 生到2个男孩为止
    3. 固定生育数量
    """

    def __init__(self, initial_couples, max_children, strategy=None):
        """
        初始化性别比例模拟

        参数:
        initial_couples: int - 初始夫妻数量
        max_children: int - 每个家庭最大生育数量
        strategy: dict - 生育策略字典
            - type: str - 策略类型 ('stop_at_boy', 'stop_at_two_boys', 'fixed_children')
            - number: int - 仅在fixed_children策略时需要，指定固定生育数量
        """
        self.initial_couples = initial_couples
        self.max_children = max_children

        # 设置默认策略（生到男孩为止）
        if strategy is None:
            self.strategy = {'type': 'stop_at_boy'}
        else:
            self.strategy = strategy

        # 验证策略参数的有效性
        self._validate_strategy()

        # 初始化随机种子，确保结果可重现
        random.seed(42)
        np.random.seed(42)

    def _validate_strategy(self):
        """验证策略参数的有效性"""
        valid_strategy_types = ['stop_at_boy', 'stop_at_two_boys', 'fixed_children']

        # 检查策略类型是否有效
        if self.strategy.get('type') not in valid_strategy_types:
            raise ValueError(
                f"无效的策略类型: {self.strategy.get('type')}\n"
                f"有效类型包括: {', '.join(valid_strategy_types)}"
            )

        # 检查固定生育数量策略的参数
        if self.strategy['type'] == 'fixed_children':
            if 'number' not in self.strategy:
                raise ValueError("fixed_children策略必须指定'number'参数")

            number = self.strategy['number']
            if not isinstance(number, int) or number <= 0:
                raise ValueError(f"fixed_children策略的number必须是正整数，当前值: {number}")

            if number > self.max_children:
                raise ValueError(
                    f"fixed_children策略的number({number})不能超过max_children({self.max_children})"
                )

    def simulate_single_family(self):
        """
        根据当前策略模拟单个家庭的生育过程

        返回:
        tuple: (男孩数量, 女孩数量)
        """
        boys = 0
        girls = 0
        strategy_type = self.strategy['type']

        if strategy_type == 'stop_at_boy':
            # 策略1：生到男孩为止
            while boys == 0 and (boys + girls) < self.max_children:
                if random.random() < 0.5:
                    boys += 1
                else:
                    girls += 1

        elif strategy_type == 'stop_at_two_boys':
            # 策略2：生到2个男孩为止
            while boys < 2 and (boys + girls) < self.max_children:
                if random.random() < 0.5:
                    boys += 1
                else:
                    girls += 1

        elif strategy_type == 'fixed_children':
            # 策略3：固定生育数量
            fixed_number = self.strategy['number']
            # 确保不超过最大生育限制
            actual_children = min(fixed_number, self.max_children)

            for _ in range(actual_children):
                if random.random() < 0.5:
                    boys += 1
                else:
                    girls += 1

        return boys, girls

    def run(self, runs=1):
        """
        运行多次模拟实验

        参数:
        runs: int - 模拟实验次数

        返回:
        list: 每次实验的结果字典列表
        """
        all_results = []

        for run in range(runs):
            total_boys = 0
            total_girls = 0
            family_sizes = []

            # 模拟每个家庭
            for _ in range(self.initial_couples):
                boys, girls = self.simulate_single_family()
                total_boys += boys
                total_girls += girls
                family_sizes.append(boys + girls)

            # 计算统计数据
            total_children = total_boys + total_girls
            boy_ratio = total_boys / total_children if total_children > 0 else 0

            # 保存结果
            result = {
                'run': run + 1,
                'total_families': self.initial_couples,
                'total_boys': total_boys,
                'total_girls': total_girls,
                'total_children': total_children,
                'boy_ratio': boy_ratio,
                'girl_ratio': 1 - boy_ratio,
                'avg_family_size': np.mean(family_sizes),
                'std_family_size': np.std(family_sizes),
                'strategy': self.strategy.copy(),
                'max_children': self.max_children
            }

            all_results.append(result)

        return all_results

    def get_summary_statistics(self, results):
        """
        计算多次模拟的汇总统计

        参数:
        results: list - run()方法返回的结果列表

        返回:
        dict - 汇总统计数据
        """
        if not results:
            return {}

        boy_ratios = [r['boy_ratio'] for r in results]
        avg_family_sizes = [r['avg_family_size'] for r in results]

        return {
            'avg_boy_ratio': np.mean(boy_ratios),
            'std_boy_ratio': np.std(boy_ratios),
            'min_boy_ratio': np.min(boy_ratios),
            'max_boy_ratio': np.max(boy_ratios),
            'avg_family_size': np.mean(avg_family_sizes),
            'std_family_size': np.std(avg_family_sizes),
            'total_runs': len(results),
            'strategy': self.strategy.copy()
        }

    def print_results(self, results):
        """
        打印模拟结果

        参数:
        results: list - run()方法返回的结果列表
        """
        print(f"\n=== 性别比例模拟结果 (策略: {self.strategy['type']}) ===")
        print(f"初始夫妻数量: {self.initial_couples}")
        print(f"最大生育数量: {self.max_children}")
        print(f"模拟次数: {len(results)}")

        if self.strategy['type'] == 'fixed_children':
            print(f"固定生育数量: {self.strategy['number']}")

        print("\n各次模拟结果:")
        print("-" * 80)
        print(f"{'次数':<4} {'男孩数':<8} {'女孩数':<8} {'总孩子数':<10} {'男孩比例':<10} {'平均家庭规模':<12}")
        print("-" * 80)

        for result in results:
            print(f"{result['run']:<4} {result['total_boys']:<8} {result['total_girls']:<8} "
                  f"{result['total_children']:<10} {result['boy_ratio']:.3f}        "
                  f"{result['avg_family_size']:.2f}")

        # 打印汇总统计
        summary = self.get_summary_statistics(results)
        print("-" * 80)
        print("汇总统计:")
        print(f"平均男孩比例: {summary['avg_boy_ratio']:.3f} (±{summary['std_boy_ratio']:.3f})")
        print(f"男孩比例范围: {summary['min_boy_ratio']:.3f} - {summary['max_boy_ratio']:.3f}")
        print(f"平均家庭规模: {summary['avg_family_size']:.2f} (±{summary['std_family_size']:.2f})")