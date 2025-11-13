import random
import numpy as np


class GenderRatioSimulation:
    def __init__(self, initial_couples=10000, max_children=None):
        """
        性别比例模拟实验

        参数:
        initial_couples: 初始夫妻对数
        max_children: 最大生育数量限制（None表示无限制）
        """
        self.initial_couples = initial_couples
        self.max_children = max_children

    def simulate_single_family(self):
        """模拟单个家庭的生育过程"""
        boys = 0
        girls = 0

        while boys == 0:
            # 检查是否达到最大生育限制
            if self.max_children is not None and (boys + girls) >= self.max_children:
                break

            # 50%概率生男孩或女孩
            if random.random() < 0.5:
                boys += 1
            else:
                girls += 1

        return boys, girls

    def run_simulation(self, num_simulations=100):
        """运行多次模拟实验"""
        results = []

        for sim in range(num_simulations):
            total_boys = 0
            total_girls = 0
            family_sizes = []
            girls_before_boy = []

            for _ in range(self.initial_couples):
                boys, girls = self.simulate_single_family()
                total_boys += boys
                total_girls += girls
                family_sizes.append(boys + girls)
                girls_before_boy.append(girls)

            total_children = total_boys + total_girls
            boy_ratio = total_boys / total_children if total_children > 0 else 0

            results.append({
                'simulation': sim + 1,
                'total_boys': total_boys,
                'total_girls': total_girls,
                'total_children': total_children,
                'boy_ratio': boy_ratio,
                'girl_ratio': 1 - boy_ratio,
                'gender_ratio': total_boys / total_girls if total_girls > 0 else float('inf'),
                'avg_family_size': np.mean(family_sizes),
                'max_family_size': max(family_sizes),
                'min_family_size': min(family_sizes),
                'family_sizes': family_sizes,
                'girls_before_boy': girls_before_boy
            })

            # 打印进度
            print(f"模拟 {sim + 1}/{num_simulations} 完成: 男孩={total_boys}, 女孩={total_girls}, 比例={boy_ratio:.4f}")

        return results

