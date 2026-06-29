from location.service import LocationService

service = LocationService()

cities = service.search_cities("Del")

print(cities)