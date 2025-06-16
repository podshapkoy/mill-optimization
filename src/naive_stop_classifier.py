"""
Анализирует спад тока перед остановкой, классифицируя на:
- emergency (аварийная) - быстрый спад (<1 мин)
- planned (плановая) - устойчивый спад (1-10 мин) до 10% от среднего
- indefinite (неопределенная) - другие случаи
"""

from datetime import timedelta

mean_current = df['Value'].mean()
below_threshold = df[df['Value'] < mean_current * 0.97]
stop_type = "indefinite"
drop_start = None
drop_duration = None

if not below_threshold.empty:
    for i in range(len(below_threshold)):
        current_time = below_threshold.index[i]
        next_period = df.loc[current_time:current_time + timedelta(minutes=3)]

        if all(next_period['Value'] < mean_current * 0.97):
            drop_start = current_time
            drop_zone = df.loc[drop_start:stop_time]
            final_value = drop_zone['Value'].iloc[-1]
            drop_duration = (stop_time - drop_start).total_seconds() / 60

            if drop_duration < 1:
                stop_type = "emergency"
            elif (1 <= drop_duration <= 10) and (final_value <= mean_current * 0.1):
                stop_type = "planned"
            break