import os, requests

# headers = {'Content-Type': 'application/xml'}

XML = """<xmp>
	<?xml version="1.0" encoding="UTF-8"?>
	<KH_Station>
		<History>
			<ST_ID>ADCPKH2001</ST_ID>
			<Date_Time>2022-06-10 09:20:00</Date_Time>
			<Velocity>8.222</Velocity>
			<Vmdir>274.185</Vmdir>
			<Latitude>22.545114</Latitude>
			<Longitude>120.286481</Longitude>
		</History>
	</KH_Station>
	<KH_Station>
		<History>
			<ST_ID>ADCPKH2002</ST_ID>
			<Date_Time>2022-06-10 09:30:00</Date_Time>
			<Velocity>4.632</Velocity>
			<Vmdir>193.736</Vmdir>
			<Latitude>22.549624</Latitude>
			<Longitude>120.27361</Longitude>
		</History>
	</KH_Station>
	<KH_Station>
		<History>
			<ST_ID>ADCPKH2003</ST_ID>
			<Date_Time>2022-06-10 09:30:00</Date_Time>
			<Velocity>4.397</Velocity>
			<Vmdir>197.199</Vmdir>
			<Latitude>22.550550</Latitude>
			<Longitude>120.274467</Longitude>
		</History>
	</KH_Station>
</xmp>"""


t = requests.post('http://203.64.168.4/dbxml.php', data=XML)
print(t.status_code)
# print(requests.post('http://203.64.168.4/dbxml.php', data=XML).text)