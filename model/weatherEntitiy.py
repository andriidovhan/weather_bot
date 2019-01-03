from weather import Weather, Unit

WEATHER = Weather(unit=Unit.CELSIUS)
base_url = "https://s.yimg.com/zz/combo?a/i/us/we/52/"


class WeatherEntity:
    def __init__(self, city):
        self.location = WEATHER.lookup_by_location(city)
        self.condition = self.location.condition

    def get_current_weather(self):
        return """temp: {}, {}""".format(self.condition.temp, self.condition.text)

    def get_forecast(self):
        forecasts_list = []
        forecasts = self.location.forecast
        for forecast in forecasts[1:6]:
            forecasts_list.append("""{}
                        Max/Min: {}/{}, {}""".format(forecast.date, forecast.high, forecast.low, forecast.text))
        return "\n".join(forecasts_list)

    def get_weather_image(self):
        return base_url + self.condition.code + ".gif"
