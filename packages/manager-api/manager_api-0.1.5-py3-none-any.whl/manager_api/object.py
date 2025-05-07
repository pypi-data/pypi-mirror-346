# -*- coding: utf-8 -*-

from __future__ import annotations

import json
import mimetypes
import os
from requests import Session
from typing import ClassVar, Dict, Optional
from uuid import UUID

from pydantic import BaseModel


class ManagerBaseModel(BaseModel):
    @classmethod
    def _get_value(cls, v, *args, **kwargs):
        if isinstance(v, Object):
            return v.Key
        elif isinstance(v, Dict):
            # JSON dictionary keys must be strings
            for k in list(v.keys()):
                if isinstance(k, Object):
                    v[str(k.Key)] = v[k]
                    del v[k]
        return super()._get_value(v, *args, **kwargs)

    def dict(self, exclude_none=True, **kwargs):
        return super().dict(exclude_none=exclude_none, **kwargs)

    def json(self, exclude_none=True, models_as_dict=False, **kwargs):
        return super().json(exclude_none=exclude_none, models_as_dict=models_as_dict, **kwargs)

    class Config:
        fields = {
            "Timestamp": {"exclude": True},
        }


class Object(ManagerBaseModel):
    _session: ClassVar[Session]
    Key: Optional[UUID]
    Name: Optional[str]
    Timestamp: Optional[int]

    def __init__(self, Key=None, **kwargs):
        kwargs.update({"Key": Key})
        return super().__init__(**kwargs)

    def __hash__(self):
        return hash(self.Key or self.Guid)

    def __eq__(self, other):
        try:
            return self.Key == other.Key
        except AttributeError:
            return False

    def _read_if_necessary(self, attr):
        if attr in super().__getattribute__("__fields__"):
            fs = super().__getattribute__("__fields_set__")
            if fs.difference({"Name"}).issubset({"Key", "Timestamp"}) and attr not in fs:
                self.read()

    def __getattribute__(self, attr):
        super().__getattribute__("_read_if_necessary")(attr)
        return super().__getattribute__(attr)

    def __setattr__(self, attr, value):
        super().__getattribute__("_read_if_necessary")(attr)
        super().__setattr__(attr, value)

    def __class_getitem__(cls, key):
        items = [i for i in cls.list() if key in (i.Name or "").replace("—", "-").split(" - ", 1)]
        if not items:
            raise KeyError(f"Object not found with name {key}")
        elif len(items) != 1:
            raise KeyError(f"More than one object found with name {key}")
        else:
            return items[0]

    @classmethod
    def validate(cls, value):
        if isinstance(value, str) or isinstance(value, UUID):
            value = {"Key": value}
        return super().validate(value)

    @staticmethod
    def _parse_response(response):
        result = response.json()
        if result is None or (isinstance(result, dict) and not result.get("Success", False)):
            raise RuntimeError(f"{response.request.method} {response.request.url}: {result['Error']}")
        return result

    @property
    def _path(self):
        return f"{self.Guid}/{self.Key}"

    @classmethod
    def list(cls):
        """List all of the objects of the given type."""
        response = cls._session.get(cls.Guid)
        result = response.json()
        def _parse(r):
            r.setdefault("Name", None)
            return cls.parse_obj(r)
        return [_parse(r) for r in result]

    def create(self):
        response = self._session.post(self.Guid, data=self.json())
        result = self._parse_response(response)
        self.Key = UUID(result["Key"])

    def read(self):
        result = self._session.get(self._path).json()
        result["Key"] = self.Key
        self.__init__(**result)

    def update(self):
        response = self._session.put(self._path, data=self.json())
        self._parse_response(response)

    def delete(self):
        response = self._session.delete(self._path)
        self._parse_response(response)
        self.Key = None

    def get_url(self, action="View"):
        return self._session._get_url(f"{type(self).__name__}{action}", self.Key)

    def attach_file(self, filename):
        url = self._session._get_url("NewAttachment", self.Key, b"\x0a")
        headers = {
            "Content-Type": "application/octet-stream",
            "X-File-Name": os.path.basename(filename),
            "X-File-Type": mimetypes.guess_type(filename)[0],
        }
        with open(filename, "rb") as fp:
            self._session.post(url, data=fp.read(), headers=headers)
