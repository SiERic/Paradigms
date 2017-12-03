select City.Name from
City inner join (Country inner join Capital on Country.Code = Capital.CountryCode) on Country.Code = City.CountryCode and City.Id = Capital.CityId
where Country.Name = "Malaysia";