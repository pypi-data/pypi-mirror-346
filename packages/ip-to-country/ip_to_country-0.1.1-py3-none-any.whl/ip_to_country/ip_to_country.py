import ipaddress
import os
import pickle
import bisect
import csv

class IpToCountry:
    def __init__(self, ipv4_pickle='data/ipv4_ranges.pkl', ipv6_pickle='data/ipv6_ranges.pkl', iso_csv='data/iso3166.csv'):
        with open(ipv4_pickle, 'rb') as f:
            self.ipv4_ranges = pickle.load(f)
        with open(ipv6_pickle, 'rb') as f:
            self.ipv6_ranges = pickle.load(f)

        self.ipv4_starts = [int(start) for start, _, _ in self.ipv4_ranges]
        self.country_names = self._load_country_names(iso_csv)

    @staticmethod
    def build_from_directory(directory="delegated_files", ipv4_pickle='ipv4_ranges.pkl', ipv6_pickle='ipv6_ranges.pkl'):
        ipv4_ranges = []
        ipv6_ranges = []
        for filename in os.listdir(directory):
            filepath = os.path.join(directory, filename)
            if os.path.isfile(filepath):
                with open(filepath, 'r') as file:
                    for line in file:
                        if line.startswith('#') or not line.strip():
                            continue
                        parts = line.strip().split('|')
                        if len(parts) < 7:
                            continue
                        registry, cc, record_type, start, value, date, status = parts[:7]
                        if status not in ('allocated', 'assigned'):
                            continue
                        try:
                            if record_type == 'ipv4':
                                start_ip = ipaddress.IPv4Address(start)
                                num_ips = int(value)
                                end_ip = ipaddress.IPv4Address(int(start_ip) + num_ips - 1)
                                ipv4_ranges.append((start_ip, end_ip, cc))
                            elif record_type == 'ipv6':
                                network = ipaddress.IPv6Network(f"{start}/{value}", strict=False)
                                ipv6_ranges.append((network, cc))
                        except ValueError as e:
                            print(f"Skipping invalid record: {e}")
                            continue

        with open(ipv4_pickle, 'wb') as f:
            ipv4_ranges.sort(key=lambda x: int(x[0]))
            pickle.dump(ipv4_ranges, f)
        with open(ipv6_pickle, 'wb') as f:
            pickle.dump(ipv6_ranges, f)

    @staticmethod
    def _load_country_names(csv_path):
        country_map = {}
        with open(csv_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if len(row) >= 2:
                    code = row[0].strip()
                    name = row[1].strip().strip('"')
                    country_map[code] = name
        return country_map

    def ip_to_country(self, ip):
        ip_obj = ipaddress.ip_address(ip)
        if isinstance(ip_obj, ipaddress.IPv4Address):
            cc = self._lookup_ipv4(ip_obj)
        elif isinstance(ip_obj, ipaddress.IPv6Address):
            cc = self._lookup_ipv6(ip_obj)
        else:
            raise ValueError("Unsupported IP address type")

        name = self.country_names.get(cc, "Unknown") if cc else "Unknown"
        return {'country_code': cc if cc else None, 'country_name': name}

    def _lookup_ipv4(self, ip_obj):
        ip_int = int(ip_obj)
        idx = bisect.bisect_right(self.ipv4_starts, ip_int) - 1
        if 0 <= idx < len(self.ipv4_ranges):
            start_ip, end_ip, cc = self.ipv4_ranges[idx]
            if start_ip <= ip_obj <= end_ip:
                return cc
        return None

    def _lookup_ipv6(self, ip_obj):
        for network, cc in self.ipv6_ranges:
            if ip_obj in network:
                return cc
        return None
