import os
from datetime import datetime
from typing import Optional, List

from fastapi import HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.models.project import Project
from app.models.record import Record
from app.models.user import User
from app.schemas.message import MessageCreate
from app.schemas.record import GetRecordResponse, GetAllRecordResponse, UpdateRecord
from app.services.ai_service import process_screenshots
from app.services.message_service import MessageService


class RecordService:
    def __init__(self, db: Session, current_user: User):
        self.db = db
        self.current_user: Optional[User] = current_user

    async def create_image_record(
            self,
            screenshots: List[UploadFile],
            project_id: Optional[int]
    ) -> GetRecordResponse:
        if not screenshots:
            raise HTTPException(status_code=400, detail="Please upload at least 1 image")
        dsl = await process_screenshots(screenshots)
        if not self._is_project_exist(project_id):
            project_id = None
        screenshot_url = await self._upload_image_to_disk(screenshots[0])
        # Save record to DB
        db_record = Record(
            screenshot_path=screenshot_url,
            dsl_content=dsl,
            user_id=self.current_user.id,
            project_id=project_id,
            created_at=datetime.utcnow()
        )
        self.db.add(db_record)
        self.db.commit()
        self.db.refresh(db_record)

        return GetRecordResponse.from_record(db_record)

    def create_dsl_record(
            self,
            dsl_content: str,
            project_id: Optional[int]
    ) -> GetRecordResponse:
        if not dsl_content.strip():
            raise HTTPException(status_code=400, detail="DSL content must not be empty")
        if not self._is_project_exist(project_id):
            project_id = None
        is_v(dsl_content)
        db_record = Record(
            screenshot_path=None,
            dsl_content=dsl_content,
            user_id=self.current_user.id,
            project_id=project_id,
            created_at=datetime.utcnow()
        )
        self.db.add(db_record)
        self.db.commit()
        self.db.refresh(db_record)

        return GetRecordResponse.from_record(db_record)

    def create_prompt_record(self, prompt: str, project_id: int) -> GetRecordResponse:
        db_record = self.create_dsl_record(dsl_content="row{}", project_id=project_id)
        message_Service = MessageService(self.db)
        msg = message_Service.send_message(
            db_record.record_id,
            MessageCreate(
                content=prompt
            ))
        return self.update_record(
            db_record.record_id,
            UpdateRecord(
                dsl_content=msg.code
            )
        )

    def get_records_with_no_project(self) -> GetAllRecordResponse:
        records = (
            self.db.query(Record)
            .filter(Record.user_id == self.current_user.id, Record.project_id.is_(None))
            .order_by(Record.created_at.asc())
            .all()
        )
        response_records = [GetRecordResponse.from_record(record) for record in records]
        numberOfRecords = len(response_records) if response_records else 0
        return GetAllRecordResponse(numberOfRecords=numberOfRecords, records=response_records)

    def get_single_record(
            self,
            record_id: int,
    ) -> GetRecordResponse:
        db_record = self._get_record(record_id)
        return GetRecordResponse.from_record(db_record)

    def update_record(
            self,
            record_id: int,
            updateRecord: UpdateRecord
    ) -> GetRecordResponse:
        db_record = self._get_record(record_id)
        is_compilable(updateRecord.dsl_content)
        db_record.dsl_content = updateRecord.dsl_content
        db_record.created_at = datetime.utcnow()
        self.db.commit()
        self.db.refresh(db_record)
        return GetRecordResponse.from_record(db_record)

    def delete_record(
            self,
            record_id: int,
    ):
        db_record = self._get_record(record_id)
        self._remove_image_from_disk_if_exist(db_record.screenshot_path)
        self.db.delete(db_record)
        self.db.commit()
        return {"detail": "Record deleted"}

    @staticmethod
    def _remove_image_from_disk_if_exist(screenshot_path):
        if screenshot_path:
            file_path = screenshot_path.lstrip("/uploads/")
            full_path = os.path.join("uploads", file_path)
            if os.path.exists(full_path):
                os.remove(full_path)

    def _get_record(self, record_id: int):
        db_record = self.db.query(Record).filter(
            Record.id == record_id, Record.user_id == self.current_user.id
        ).first()

        if not db_record:
            raise HTTPException(status_code=404, detail="Record not found")
        return db_record

    def _get_project(self, project_id: int):
        db_project = self.db.query(Project).filter(Project.id == project_id,
                                                   Project.user_id == self.current_user.id).first()
        if not db_project:
            raise HTTPException(status_code=404, detail="Project not found")
        return db_project

    def _is_project_exist(self, project_id: int):
        db_project = self.db.query(Project).filter(Project.id == project_id,
                                                   Project.user_id == self.current_user.id).first()
        if not db_project:
            return False
        else:
            return True

    @staticmethod
    async def _upload_image_to_disk(screenshot):
        filename = f"{datetime.utcnow().timestamp()}_{screenshot.filename}"
        file_path = os.path.join("uploads", filename)
        os.makedirs("uploads", exist_ok=True)
        await screenshot.seek(0)
        with open(file_path, "wb") as f:
            f.write(await screenshot.read())
        return f"/uploads/{filename}"
