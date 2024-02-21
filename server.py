import json

from aiohttp import web
from sqlalchemy.exc import IntegrityError

from models import Session, Announcement, engine, init_orm

app = web.Application()


@web.middleware
async def session_middleware(request, handler):
    async with Session() as session:
        request.session = session
        response = await handler(request)
        return response


async def orm_context(app):
    print('STARTING')
    await init_orm()
    yield
    await engine.dispose()
    print('ENDING')


app.cleanup_ctx.append(orm_context)
app.middlewares.append(session_middleware)


def get_error(error_class, message):
    return error_class(
        text=json.dumps(
            {'error': message}
        ),
        content_type='application/json'
    )


async def get_announcement_by_id(session, announcement_id):
    announcement = await session.get(Announcement, announcement_id)
    if announcement is None:
        raise get_error(web.HTTPNotFound, f'Announcement with id {announcement_id} not found')
    return announcement


async def add_announcement(session, announcement):
    try:
        session.add(announcement)
        await session.commit()
    except IntegrityError:
        raise get_error(web.HTTPConflict, message=f'Announcement with title {announcement.title} already exists')
    return announcement.id


class AnnouncementView(web.View):

    @property
    def announcement_id(self):
        return int(self.request.match_info['announcement_id'])

    @property
    def session(self) -> Session:
        return self.request.session

    async def get_announcement(self):
        announcement = await get_announcement_by_id(self.session, self.announcement_id)
        return announcement

    async def get(self):
        announcement = await self.get_announcement()
        return web.json_response(announcement.dict)

    async def post(self):
        announcement_data = await self.request.json()
        announcement = Announcement(**announcement_data)
        await add_announcement(self.session, announcement)
        return web.json_response({'id': announcement.id})

    async def patch(self):
        announcement_data = await self.request.json()
        announcement = await self.get_announcement()

        for key, value in announcement_data.items():
            setattr(announcement, key, value)
        await add_announcement(self.session, announcement)
        return web.json_response({'id': announcement.id})

    async def delete(self):
        announcement = await self.get_announcement()
        await self.session.delete(announcement)
        await self.session.commit()
        return web.json_response({'status': 'deleted'})


app.add_routes(
    [
        web.get("/announcement/{announcement_id:\d+}", AnnouncementView),
        web.patch("/announcement/{announcement_id:\d+}", AnnouncementView),
        web.delete("/announcement/{announcement_id:\d+}", AnnouncementView),
        web.post("/announcement", AnnouncementView)
    ]
)

if __name__ == '__main__':
    web.run_app(app)
