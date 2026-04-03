# 咖啡浓度趋势分析系统设计方案

## 功能概述

记录用户每次鉴定的浓度值，生成趋势图表，分析咖啡摄入模式。

---

## 数据模型

### 单次记录 (CoffeeRecord)

```json
{
  "timestamp": "2026-04-03T18:14:42+08:00",  // ISO 8601格式
  "date": "2026-04-03",                       // 日期
  "time": "18:14",                            // 时间
  "concentration": 0.288,                     // 浓度值 (0.000-1.000)
  "coffee_type": "冰美式",                     // 咖啡类型
  "is_orthodox": true,                        // 是否纯正
  "strength_level": "Regular",                // 信息强度
  "story_title": "F1加速",                    // 故事标题
  "location": "办公室",                        // 地点 (可选)
  "weather": "晴",                             // 天气 (可选)
  "mood": "疲惫",                              // 心情 (可选)
  "notes": "下午提神"                          // 备注 (可选)
}
```

### 统计数据 (Statistics)

```json
{
  "total_records": 100,           // 总记录数
  "orthodox_count": 85,           // 纯正咖啡数
  "heretic_count": 15,            // 异端咖啡数
  "average_concentration": 0.352, // 平均浓度
  "max_concentration": 0.888,     // 最高浓度
  "min_concentration": 0.000,     // 最低浓度
  "most_frequent_type": "冰美式",  // 最常喝咖啡
  "streak_days": 7,               // 连续记录天数
  "last_record_date": "2026-04-03" // 最后记录日期
}
```

---

## 趋势图表类型

### 1. 日浓度曲线 (Daily Concentration Curve)

**用途**: 展示一天内的浓度变化

```
浓度
  ↑
1.0│                    ●───●
   │                 ╱
0.5│    ●────●────●
   │ ╱
0.0│●
   └────────────────────────→ 时间
     8:00   12:00  15:00  18:00
```

** Insights **:
- 早晨浓度低（唤醒）
- 下午浓度高（提神）
- 深夜异端警告（NONSENSE）

---

### 2. 周趋势图 (Weekly Trend)

**用途**: 展示一周的浓度趋势

```
浓度
  ↑
1.0│         ┌───┐
   │    ┌───┐│   │┌───┐
0.5│┌───┐   ││   ││   │┌───┐
   ││   │   ││   ││   ││   │
0.0│└───┘   └┘   └┘   └┘   └───
   └────────────────────────→ 星期
     一   二   三   四   五   六   日
```

**Insights**:
- 工作日 vs 周末模式
- 周一综合征（浓度高）
- 周五放松（浓度低/异端）

---

### 3. 浓度分布饼图 (Concentration Distribution)

**用途**: 展示浓度区间分布

```
      Lite (0-0.25)
         25%
           ╱╲
          ╱  ╲
Regular ╱    ╲ Strong
(0.25-0.5)╲    ╱ (0.5-0.75)
    40%    ╲  ╱   20%
            ╲╱
         NONSENSE
         (异端) 15%
```

---

### 4. 纯正vs异端对比 (Orthodox vs Heretic)

**用途**: 展示咖啡纯度坚持度

```
纯正咖啡  ████████████████████ 85%
异端咖啡  ████ 15%

[████████░░░░░░░░░░] 纯度坚持度: 85%
```

---

### 5. 连续打卡记录 (Streak Calendar)

**用途**: 类似GitHub贡献图的打卡记录

```
          一 二 三 四 五 六 日
    3月  ░░ ██ ██ ██ ██ ░░ ░░
         ██ ██ ██ ██ ██ ██ ██
    4月  ██ ██ ██ ░░ ██ ░░ ░░

图例: ██ 有记录  ░░ 无记录  🟥 异端日
```

---

## 趋势生成脚本

```python
import json
from datetime import datetime, timedelta
from collections import defaultdict
import matplotlib.pyplot as plt

class CoffeeTrendAnalyzer:
    def __init__(self, user_data_path):
        with open(user_data_path, 'r') as f:
            self.data = json.load(f)
        self.records = self.data['records']
    
    def get_daily_trend(self, days=7):
        """获取最近N天的趋势"""
        daily_data = defaultdict(list)
        
        for record in self.records:
            date = record['date']
            if record['concentration'] is not None:
                daily_data[date].append(record['concentration'])
        
        # 计算每日平均
        trend = {}
        for date, concentrations in daily_data.items():
            trend[date] = sum(concentrations) / len(concentrations)
        
        return trend
    
    def get_strength_distribution(self):
        """获取信息强度分布"""
        distribution = defaultdict(int)
        
        for record in self.records:
            level = record['strength_level']
            distribution[level] += 1
        
        return dict(distribution)
    
    def get_orthodox_ratio(self):
        """获取纯正比例"""
        orthodox = sum(1 for r in self.records if r['is_orthodox'])
        total = len(self.records)
        return orthodox / total if total > 0 else 0
    
    def generate_weekly_report(self):
        """生成周报"""
        week_data = self.get_daily_trend(days=7)
        
        report = {
            'period': '最近7天',
            'total_coffees': len(self.records),
            'avg_concentration': sum(r['concentration'] or 0 for r in self.records) / len(self.records),
            'orthodox_ratio': self.get_orthodox_ratio(),
            'max_concentration_day': max(week_data.items(), key=lambda x: x[1]),
            'heretic_incidents': sum(1 for r in self.records if not r['is_orthodox'])
        }
        
        return report
    
    def export_chart(self, chart_type='daily', output_path='chart.png'):
        """导出趋势图表"""
        if chart_type == 'daily':
            self._plot_daily_trend(output_path)
        elif chart_type == 'distribution':
            self._plot_distribution(output_path)
        elif chart_type == 'orthodox':
            self._plot_orthodox_ratio(output_path)
    
    def _plot_daily_trend(self, output_path):
        """绘制日趋势图"""
        trend = self.get_daily_trend()
        dates = sorted(trend.keys())
        values = [trend[d] for d in dates]
        
        plt.figure(figsize=(10, 6))
        plt.plot(dates, values, marker='o', linewidth=2, color='#3D2314')
        plt.axhline(y=0.25, color='gray', linestyle='--', alpha=0.5, label='星巴克标准')
        plt.xlabel('日期')
        plt.ylabel('平均浓度')
        plt.title('咖啡浓度趋势')
        plt.legend()
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(output_path)
        plt.close()

# 使用示例
analyzer = CoffeeTrendAnalyzer('user-coffee-history.json')
report = analyzer.generate_weekly_report()
print(report)
analyzer.export_chart('daily', 'daily_trend.png')
```

---

## 用户报告示例

### 周报

```
═══════════════════════════════════
    ☕ 美式咖啡宇宙 - 周报
═══════════════════════════════════

统计周期: 2026-03-28 至 2026-04-03

📊 本周概览
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
总杯数: 12杯
纯正咖啡: 10杯 (83%)
异端事件: 2次 (17%)
平均浓度: 0.324

📈 浓度趋势
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
周一: 0.250 ⬜ 标准启动
周二: 0.314 ⬜ 渐入佳境
周三: 0.500 ⬆ 高强度日
周四: 0.288 ⬜ 回归常态
周五: 0.125 ⬇ 放松模式
周六: NONSENSE 🟥 异端警报 (拿铁)
周日: 0.000 ⬜ 纯净水日

🏆 本周之最
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
最高浓度: 周三 0.500 (临界点)
最低浓度: 周日 0.000 (原始形态)
最异端日: 周六 (背叛了美式信仰)

📅 连续打卡: 7天 🔥
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[████████████████████] 100%

下周建议: 保持纯正，减少异端！
═══════════════════════════════════
```

---

## 数据存储方案

### 方案A: JSON文件（MVP阶段）
- 优点: 简单，无需数据库
- 缺点: 查询效率低
- 适用: 个人用户，记录<1000条

### 方案B: SQLite（扩展阶段）
- 优点: 结构化查询，高效
- 缺点: 需要额外依赖
- 适用: 多用户，记录>1000条

### 方案C: 云数据库（产品化阶段）
- 优点: 云端同步，多设备
- 缺点: 成本
- 适用: 小程序/APP

---

## 实施步骤

### Phase 1: 基础记录（现在）
- [ ] 每次鉴定自动记录到JSON
- [ ] 基础统计（总数、平均值）
- [ ] 简单文本报告

### Phase 2: 可视化（后续）
- [ ] 生成趋势图表
- [ ] 周报/月报自动发送
- [ ] 打卡日历

### Phase 3: 智能化（未来）
- [ ] 浓度预测（基于历史）
- [ ] 健康建议（摄入提醒）
- [ ] 社交功能（好友排名）

---

## 隐私考虑

1. **数据本地存储**: 默认存储在用户本地
2. **可选云同步**: 用户主动选择上传
3. **数据导出**: 支持导出JSON备份
4. **数据清除**: 支持一键清除历史

---

## 代码集成

在现有图片生成脚本中增加记录功能：

```python
def generate_certificate(user_id, photo_path, coffee_type, concentration, is_orthodox):
    # 1. 生成鉴定卡图片
    card_path = create_image(photo_path, coffee_type, concentration, is_orthodox)
    
    # 2. 记录到历史
    record = {
        'timestamp': datetime.now().isoformat(),
        'concentration': concentration,
        'coffee_type': coffee_type,
        'is_orthodox': is_orthodox,
        # ...
    }
    save_to_history(user_id, record)
    
    # 3. 返回图片
    return card_path
```
