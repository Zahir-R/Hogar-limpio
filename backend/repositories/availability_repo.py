from shared.firebase import db


class AvailabilityRepository:
    def get_template(self, worker_uid):
        doc = db.collection("availability_templates").document(worker_uid).get()
        return doc.to_dict() if doc.exists else {}

    def set_template(self, worker_uid, data):
        db.collection("availability_templates").document(worker_uid).set(data, merge=True)

    def get_override(self, worker_uid, date):
        doc = (
            db.collection("availability")
            .document(worker_uid)
            .collection("overrides")
            .document(date)
            .get()
        )
        return doc.to_dict() if doc.exists else None

    def set_override(self, worker_uid, date, data):
        ref = (
            db.collection("availability")
            .document(worker_uid)
            .collection("overrides")
            .document(date)
        )
        ref.set(data)

    def delete_override(self, worker_uid, date):
        (
            db.collection("availability")
            .document(worker_uid)
            .collection("overrides")
            .document(date)
            .delete()
        )

    def get_overrides_for_range(self, worker_uid, dates):
        overrides = {}
        for d in dates:
            override = self.get_override(worker_uid, d)
            if override:
                overrides[d] = override
        return overrides
