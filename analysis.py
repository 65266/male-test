import matplotlib.pyplot as plt
import numpy as np
from scipy import stats


def analyze_results(results):
    """分析模拟结果"""
    # 计算统计指标
    boy_ratios = [r['boy_ratio'] for r in results]
    gender_ratios = [r['gender_ratio'] for r in results]
    avg_family_sizes = [r['avg_family_size'] for r in results]

    stats_summary = {
        'mean_boy_ratio': np.mean(boy_ratios),
        'std_boy_ratio': np.std(boy_ratios),
        'mean_gender_ratio': np.mean(gender_ratios),
        'std_gender_ratio': np.std(gender_ratios),
        'mean_family_size': np.mean(avg_family_sizes),
        'confidence_interval': stats.t.interval(0.95, len(boy_ratios) - 1,
                                                loc=np.mean(boy_ratios),
                                                scale=stats.sem(boy_ratios))
    }

    return stats_summary


def plot_results(results, stats_summary):
    """绘制结果图表"""
    boy_ratios = [r['boy_ratio'] for r in results]
    gender_ratios = [r['gender_ratio'] for r in results]

    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))

    # 1. 男孩比例变化趋势
    ax1.plot(range(1, len(results) + 1), boy_ratios, 'b-', linewidth=1)
    ax1.axhline(y=0.5, color='r', linestyle='--', alpha=0.7, label='理论值 0.5')
    ax1.axhline(y=stats_summary['mean_boy_ratio'], color='g', linestyle='-',
                alpha=0.7, label=f'平均值 {stats_summary["mean_boy_ratio"]:.4f}')
    ax1.fill_between(range(1, len(results) + 1),
                     stats_summary['confidence_interval'][0],
                     stats_summary['confidence_interval'][1],
                     alpha=0.2, color='gray', label='95%置信区间')
    ax1.set_title('男孩比例变化趋势')
    ax1.set_xlabel('模拟次数')
    ax1.set_ylabel('男孩比例')
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # 2. 男孩比例分布直方图
    ax2.hist(boy_ratios, bins=20, alpha=0.7, color='skyblue', edgecolor='black')
    ax2.axvline(x=0.5, color='r', linestyle='--', alpha=0.7, label='理论值 0.5')
    ax2.axvline(x=stats_summary['mean_boy_ratio'], color='g', linestyle='-',
                alpha=0.7, label=f'平均值 {stats_summary["mean_boy_ratio"]:.4f}')
    ax2.set_title('男孩比例分布')
    ax2.set_xlabel('男孩比例')
    ax2.set_ylabel('频次')
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    # 3. 家庭规模分布
    all_family_sizes = []
    for r in results:
        all_family_sizes.extend(r['family_sizes'])

    size_counts = {}
    for size in all_family_sizes:
        size_counts[size] = size_counts.get(size, 0) + 1

    sizes = sorted(size_counts.keys())
    counts = [size_counts[s] for s in sizes]

    ax3.bar(sizes[:10], counts[:10], color='lightcoral', alpha=0.7)
    ax3.set_title('家庭规模分布（前10种）')
    ax3.set_xlabel('家庭规模（孩子数量）')
    ax3.set_ylabel('家庭数量')
    ax3.grid(True, alpha=0.3, axis='y')

    # 4. 男女比例散点图
    ax4.scatter(range(1, len(results) + 1), gender_ratios, alpha=0.6, color='purple')
    ax4.axhline(y=1.0, color='r', linestyle='--', alpha=0.7, label='平衡比例 1.0')
    ax4.axhline(y=stats_summary['mean_gender_ratio'], color='g', linestyle='-',
                alpha=0.7, label=f'平均比例 {stats_summary["mean_gender_ratio"]:.4f}')
    ax4.set_title('男女比例变化')
    ax4.set_xlabel('模拟次数')
    ax4.set_ylabel('男女比例（男孩/女孩）')
    ax4.legend()
    ax4.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.show()

    return fig


def print_summary(stats_summary):
    """打印统计摘要"""
    print("\n=== 实验结果统计摘要 ===")
    print(f"平均男孩比例: {stats_summary['mean_boy_ratio']:.6f} ± {stats_summary['std_boy_ratio']:.6f}")
    print(
        f"95%置信区间: [{stats_summary['confidence_interval'][0]:.6f}, {stats_summary['confidence_interval'][1]:.6f}]")
    print(f"平均男女比例: {stats_summary['mean_gender_ratio']:.6f} ± {stats_summary['std_gender_ratio']:.6f}")
    print(f"平均家庭规模: {stats_summary['mean_family_size']:.2f}")
