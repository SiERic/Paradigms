select Begin.Year, End.Year, Country.Name, 1.0 * (End.Rate - Begin.Rate) / (End.Year - Begin.Year)
from Country inner join LiteracyRate Begin on Country.Code = Begin.CountryCode inner join LiteracyRate End on Country.Code = End.CountryCode and End.Year > Begin.Year
group by Country.Name, Begin.Year having End.Year = min(End.Year)
order by 1.0 * (End.Rate - Begin.Rate) / (End.Year - Begin.Year) desc;