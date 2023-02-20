import json

from models.custom_model import DB_CLIENT, collection_names


class DBHandler:
    @staticmethod
    def export_json() -> str:
        json_data = {}
        for model, coll_name in collection_names.items():
            entry_list = []
            all_entries = model.all()
            for entry in all_entries:
                entry_list.append(entry.encode())
            json_data[coll_name] = entry_list
        return json.dumps(json_data, ensure_ascii=True)

    @staticmethod
    def import_json(json_data: dict):
        for coll_name, entries in json_data.items():
            for entry in entries:
                DB_CLIENT.save(coll_name, entry)

    @staticmethod
    def drop_all():
        for model, coll_name in collection_names.items():
            all_entries = model.all()
            for entry in all_entries:
                DB_CLIENT.delete(coll_name, str(entry.uuid))
