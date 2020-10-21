from pathlib import Path

if __name__ == '__main__':
    geoname_fp = Path(__file__, '..', 'allCountries.txt').resolve()
    country_name_fp = Path(__file__, '..', 'CountriesNamesAlt.txt').resolve()
    unique_names = set()
    with geoname_fp.open('r') as geonames_file:
        for line in geonames_file:
            line = line.strip()
            split_line = line.split('\t')
            country_name = split_line[1]
            unique_names.add(country_name)
            alt_names = split_line[3].split(',')
            for alt_name in alt_names:
                unique_names.add(alt_name)
    with country_name_fp.open('w+') as country_name_file:
        for name in unique_names:
            country_name_file.write(f'{name}\n')