#!/usr/bin/env python

from weather import Weather, Unit

weather = Weather(unit=Unit.CELSIUS)

location = weather.lookup_by_location('kharkiv')
condition = location.condition
print("Today is: {}".format(condition.date))
print("Current temp: {}".format(condition.temp))
print("Summary: {}".format(condition.text))
print(20*"=")


forecasts = location.forecast
for forecast in forecasts[:2]:
    print(forecast.date)
    print("Max/Min: {}/{}".format(forecast.high, forecast.low))
    print("Summary: {}".format(forecast.text))