import scrapy
import csv

class EarthquakeSpider(scrapy.Spider):
    name = 'earthquake'
    start_urls = ['https://www.bmkg.go.id/gempabumi-dirasakan.html']

    def parse(self, response):
        # Extract the header row
        header_row = response.xpath('//table/thead/tr/th')[1:]
        header_row = [th.xpath('text()').get() for th in header_row]

        # Extract the data rows and avoid duplicates
        data_rows = response.xpath('//table/tbody/tr')
        data = []
        seen_rows = set()
        for row in data_rows:
            row_data = []
            for td in row.xpath('td'):
                row_data.append(td.xpath('text()').get())
            # Check if the row has already been extracted
            row_tuple = tuple(row_data)
            if row_tuple not in seen_rows:
                # Extract the time date from the second column
                time_date = row.xpath('td[2]//text()').get()
                # Extract the latitude longitude from the third column
                latitude_longitude = row.xpath('td[3]//text()').get()
                # Extract the magnitude from the fourth column
                magnitude = row.xpath('td[4]//text()').get()
                # Extract the depth from the fifth column
                depth = row.xpath('td[5]//text()').getall()
                # Extract the MMI data from the sixth column
                mmi_data = row.xpath('td[6]/a//text()').get()
                # Combine all data into a single list
                row_data = time_date.split() + latitude_longitude [magnitude] + [depth] +  [mmi_data]
                data.append(row_data)
                seen_rows.add(row_tuple)

        # Save data as CSV
        with open('earthquake_data.csv', mode='w', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(header_row)
            writer.writerows(data)
