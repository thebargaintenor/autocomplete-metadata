#!/usr/bin/env python3

from sqlalchemy import (
    create_engine,
    func
)
from sqlalchemy.orm import (
    Query,
    sessionmaker
)
from sqlalchemy.util import KeyedTuple

from search_models import (
    Author,
    Course,
    CourseAuthorMapping,
    CourseModuleMapping,
    Module,
    ModuleClipMapping,
    Clip
)

import config
import json
import sys

# REMOVE CREDS BEFORE COMMIT
host = config.host
username = config.username
password = config.password
database = config.database
connection_string = 'postgresql://{}:{}@{}/{}'.format(
    username, password, host, database
)

pg_engine = create_engine(connection_string)
SessionFactory = sessionmaker(bind=pg_engine)
session = SessionFactory()


def fetch_authors_query() -> Query:
    return (
        session.query(
            Author.id,
            Author.displayName.label('name')
        ).
        select_from(Author)
    )


def format_author(author: KeyedTuple) -> dict:
    return {
        'id': author.id,
        'name': author.name
    }


def fetch_courses_query() -> Query:
    return (
        session.query(
            Course.id,
            Course.deprecatedCourseId,
            Course.title,
            func.array_agg(Author.displayName).label('authors'),
            Course.description,
            Course.level,
            Course.modifiedAt.label('modified_on'),
            Course.tags,
            Course.averageRating.label('rating'),
            Course.numberOfRatings.label('number_of_ratings')
        ).
        select_from(Course).
        filter(Course.deprecatedCourseId is not None).
        filter(Course.status != 'retired').
        join(CourseAuthorMapping,
            Course.id == CourseAuthorMapping.courseId).
        join(Author,
            Author.id == CourseAuthorMapping.authorId).
        group_by(Course.id)
    )


# I think this is sufficient for courses
def format_course(course: KeyedTuple) -> dict:
    return {
        'id': course.id,
        'title': course.title,
        'deprecated_course_id': course.deprecatedCourseId,
        'authors': course.authors,
        'tags': course.tags
    }


def fetch_modules_query() -> Query:
    return (
        session.query(
            Module.id,
            Module.deprecatedModuleId,
            Module.title,
            Module.updatedAt.label('updated_on'),
            Course.id.label('course_id'),
            Course.title.label('course_title'),
            Course.deprecatedCourseId.label('deprecated_course_id'),
            Course.modifiedAt.label('course_modified_on'),
            CourseModuleMapping.modulePosition.label('position')
        ).
        select_from(Module).
        join(CourseModuleMapping,
            CourseModuleMapping.moduleId == Module.id).
        join(Course,
            CourseModuleMapping.courseId == Course.id).
        filter(Course.deprecatedCourseId is not None).
        filter(Course.status != 'retired')
    )


def format_module(index: str, module: KeyedTuple) -> dict:
    return {
        '_index': index,
        '_type': 'module',
        '_id': module.id,
        '_source': {
            'deprecated_module_id': module.deprecatedModuleId,
            'title': module.title,
            'updated_on': module.updated_on,
            'course_title': module.course_title,
            'course_id': module.course_id,
            'deprecated_course_id': module.deprecated_course_id,
            'modified_on': module.course_modified_on,
            'position': module.position
        }
    }


def fetch_clips_query() -> Query:
    return (
        session.query(
            Clip.id,
            Clip.title,
            Course.id.label('course_id'),
            Course.title.label('course_title'),
            Course.deprecatedCourseId.label('deprecated_course_id'),
            Course.modifiedAt.label('course_modified_on'),
            ModuleClipMapping.moduleId.label('module_id'),
            Module.deprecatedModuleId.label('deprecated_module_id'),
            Module.title.label('module_title'),
            ModuleClipMapping.clipPosition.label('position')
        ).
        select_from(Clip).
        join(ModuleClipMapping,
            ModuleClipMapping.clipId == Clip.id).
        join(Module,
            Module.id == ModuleClipMapping.moduleId).
        join(CourseModuleMapping,
            CourseModuleMapping.moduleId == ModuleClipMapping.moduleId).
        join(Course,
            CourseModuleMapping.courseId == Course.id).
        filter(Course.deprecatedCourseId is not None).
        filter(Course.status != 'retired')
    )


def format_clip(index: str, clip: KeyedTuple) -> dict:
    return {
        '_index': index,
        '_type': 'clip',
        '_id': clip.id,
        '_source': {
            'title': clip.title,
            'course_title': clip.course_title,
            'deprecated_course_id': clip.deprecated_course_id,
            'course_id': clip.course_id,
            'modified_on': clip.course_modified_on,
            'deprecated_module_id': clip.deprecated_module_id,
            'module_title': clip.module_title,
            'module_id': clip.module_id,
            'position': clip.position
        }
    }


def main():
    output_file_name = sys.argv[1]
    courses = fetch_courses_query().yield_per(1000)
    authors = fetch_authors_query().yield_per(50)
    course_dict = {
        'courses': list(format_course(c) for c in courses),
        'authors': list(format_author(a) for a in authors)
    }
    with open(output_file_name, 'w') as output_file:
        json.dump(course_dict, output_file)


if __name__ == '__main__':
    main()
