select Country.Name, count(City.Name)
from Country left join City
on Country.Code = City.CountryCode and City.Population >= 1000000
group by Country.Name
order by count(City.Name) desc, Country.Name;