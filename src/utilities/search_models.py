#!/usr/bin/env python3

from sqlalchemy import (
    Column,
    PrimaryKeyConstraint
)

from sqlalchemy.types import (
    Boolean,
    Integer,
    Text,
    DateTime,
    JSON
)

from sqlalchemy.dialects.postgresql import (
    DOUBLE_PRECISION,
    UUID
)

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Course(Base):
    __tablename__ = 'courses'
    averageRating = Column(DOUBLE_PRECISION)
    commissionedAt = Column(DateTime)
    deprecatedCourseId = Column(Text)
    description = Column(Text)
    duration = Column(Text)
    id = Column(UUID, primary_key=True)
    image = Column(JSON)
    level = Column(Text)
    modifiedAt = Column(DateTime)
    numberOfRatings = Column(Integer)
    publishedAt = Column(DateTime)
    releasedAt = Column(DateTime)
    shortDescription = Column(Text)
    slug = Column(Text)
    status = Column(Text)
    tags = Column(JSON)
    title = Column(Text)
    retired = Column(JSON)
    updatedAt = Column(DateTime)
    hasTranscript = Column(Boolean)
    displayDate = Column(DateTime)


class CourseAuthorMapping(Base):
    __tablename__ = 'coursesAuthors'
    authorId = Column(UUID, primary_key=True)
    courseId = Column(UUID, primary_key=True)


class CourseModuleMapping(Base):
    __tablename__ = 'coursesModules'
    courseId = Column(UUID, primary_key=True)
    moduleId = Column(UUID, primary_key=True)
    modulePosition = Column(Integer)


class Module(Base):
    __tablename__ = 'modules'
    description = Column(Text)
    id = Column(UUID, primary_key=True)
    deprecatedModuleId = Column(Text)
    slug = Column(Text)
    title = Column(Text)
    updatedAt = Column(DateTime)


class ModuleClipMapping(Base):
    __tablename__ = 'modulesClips'
    clipId = Column(UUID, primary_key=True)
    clipPosition = Column(Integer)
    moduleId = Column(UUID, primary_key=True)


class Clip(Base):
    __tablename__ = 'clips'
    id = Column(UUID, primary_key=True)
    title = Column(Text)
    slug = Column(Text)


class Author(Base):
    __tablename__ = 'authors'
    authorHandle = Column(Text)
    displayName = Column(Text)
    id = Column(UUID, primary_key=True)
