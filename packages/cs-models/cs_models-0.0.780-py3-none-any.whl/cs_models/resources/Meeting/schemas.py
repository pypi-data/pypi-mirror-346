from marshmallow import (
    Schema,
    fields,
    validate,
)


class MeetingResourceSchema(Schema):
    not_blank = validate.Length(min=1, error='Field cannot be blank')

    id = fields.Integer(dump_only=True)
    meeting_name = fields.String(required=True)
    start_date = fields.DateTime(required=True)
    end_date = fields.DateTime(required=True)
    tile_release_date = fields.DateTime(allow_none=True)
    abstract_release_date = fields.DateTime(allow_none=True)
    from_website = fields.Boolean(allow_none=True)
    meeting_bucket_id = fields.Integer(allow_none=True)
    author_pipeline = fields.Boolean(allow_none=True)
    insights_pipeline = fields.Boolean(allow_none=True)
    important_dates = fields.String(allow_none=True)
    indexing_status = fields.String(allow_none=True)
    status = fields.String(allow_none=True)
    updated_at = fields.DateTime()
