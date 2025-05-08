import requests
import json
from typing import List
from collections import defaultdict

import logging
logger = logging.getLogger(__name__)


class VIAFRecord:
    def __init__(self,
                 record: dict,
                 allowed_sources: List[str] = [
                     "LC", "DNB", "LNB", "NLL", "ERRR", "J9U"]
                 ):
        self.__record: dict = record
        self.__record_data: dict = {}
        self.__allowed_sources: List[str] = allowed_sources
        self.__viaf_id: int = None
        self.__name_variations: List[str] = []
        self.__birth_date: str = None
        self.__death_date: str = None
        self.__occupations: List[str] = []
        self.__all_fields: dict = {}
        self.__nationality: str = ""
        self.__has_isni: bool = False
        self.__author: str = ""
        self.__author_type: str = None
        self.__has_isni: str = ""
        self.__activity_start: str = None
        self.__activity_end: str = None

    @property
    def author(self) -> str:
        if not self.__author:
            self.__author = self.record_data.get(
                "mainHeading", {}).get("text", "")

    @property
    def author_type(self) -> str:
        """type of name (personal, corporate, title, etc)"""
        if not self.__author_type:
            self.__author_type = self.record_data.get("nameType")

    @property
    def viaf_id(self) -> int:
        if not self.__viaf_id:
            self.__viaf_id = self.record_data.get("viafID", "")
        return self.__viaf_id

    @property
    def has_isni(self) -> bool:
        return bool(self.record_data.get("isni", ""))

    def __get_data(self, field_name: str) -> List[str]:
        entries = self.record_data.get(field_name, {}).get("data", [])

        data = []
        for entry in entries:
            sources = entry.get("sources", {}).get("s", [])
            if set(self.__allowed_sources).intersection(set(sources)):
                data.append(entry.get("text", ""))
        return data

    @property
    def record_data(self) -> dict:
        if not self.__record_data:
            try:
                self.__record_data = self.__record["queryResult"]
            except:
                self.__record_data = self.__record["recordData"]["VIAFCluster"]

        return self.__record_data

    @property
    def name_variations(self) -> List[str]:
        if not self.__name_variations:
            self.__name_variations = self.__get_data("mainHeadings")
        return self.__name_variations

    @property
    def birth_date(self) -> str:
        if not self.__birth_date:
            self.__birth_date = self.record_data.get("birthDate", None)
        return self.__birth_date

    @property
    def death_date(self) -> str:
        if not self.__death_date:
            self.__death_date = self.record_data.get("deathDate", None)
        return self.__death_date

    @property
    def occupations(self) -> List[str]:
        if not self.__occupations:
            self.__occupations = self.__get_data("occupation")
        return self.__occupations

    @property
    def activity_start(self) -> str:
        if not self.__birth_date:
            self.__birth_date = self.record_data.get("activityStart", None)
        return self.__birth_date

    @property
    def activity_end(self) -> str:
        if not self.__death_date:
            self.__death_date = self.record_data.get("activityEnd", None)
        return self.__death_date

    @property
    def nationality(self) -> str:
        if not self.__nationality:
            nationalities = self.__get_data("nationalityOfEntity")
            nationalities_dict = defaultdict(int)
            for n in nationalities:
                nationalities_dict[n.lower()] += 1
            if nationalities:
                self.__nationality = sorted(
                    nationalities_dict.items(), key=lambda x: x[1], reverse=True)[0][0]
        return self.__nationality

    @property
    def all_fields(self) -> dict:
        if not self.__all_fields:
            self.__all_fields = {
                "viaf_id": self.viaf_id,
                "name_variations": self.name_variations,
                "birth_date": self.birth_date,
                "death_date": self.death_date,
                "occupations": self.occupations,
                "nationality": self.nationality,
                "activity_start": self.activity_start,
                "activity_end": self.activity_end,
                "has_isni": self.has_isni,
                "author": self.author
            }
        return self.__all_fields


class VIAFClient:
    def __init__(self, viaf_api_url: str = "https://viaf.org/api"):
        self.root_url = viaf_api_url.strip("/")
        self.record_url = f"{self.root_url}/cluster-record"
        self.search_url = f"{self.root_url}/search"
        self.headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }

    def _send_request(self, url: str, data: dict) -> dict:
        return requests.post(url, data=json.dumps(data), headers=self.headers)

    def get_records_by_search_term(self,
                                   search_term: str,
                                   index: str = "viaf",
                                   field: str = "local.names",
                                   page_index: int = 0,
                                   page_size: int = 50
                                   ) -> dict:
        data = {
            "reqValues": {
                "field": field,
                "index": index,
                "searchTerms": search_term
            },
            "meta": {
                "env": "prod",
                "pageIndex": page_index,
                "pageSize": page_size
            }
        }
        response = self._send_request(url=self.search_url, data=data)
        return response

    def get_records_by_viaf_id(self, record_id: str) -> dict:
        data = {
            "reqValues": {
                "recordId": str(record_id)
            }
        }
        response = self._send_request(url=self.record_url, data=data)

        return response

    def fetch_viaf_clusters(self, viaf_ids):

        results = {}

        for viaf_id in viaf_ids:
            try:
                response = self.get_records_by_viaf_id(viaf_id)
                response.raise_for_status()
                results[viaf_id] = response.json()
            except requests.exceptions.RequestException as e:
                logger.error(f"Error fetching VIAF record {viaf_id}: {e}")
                results[viaf_id] = {}

        return results

    def get_normalized_data(self, record_ids: List[str]) -> List[VIAFRecord]:
        """ Fetch data required for normalization from VIAF. """
        response = self.fetch_viaf_clusters(record_ids)
        return [VIAFRecord(response[record_id]) for record_id in record_ids]
