import graphene
from graphql import GraphQLError
from graphql_auth.decorators import login_required
from graphene_file_upload.scalars import Upload
from tracker.models import (
    Section, Course,
    Topic, Resource,
    TimeTable, TimeTableActivity,
    Todo, TodoItem)
from .types import (
    SectionType, CourseType,
    TopicType, ResourceType,
    TimeTableType, TimeTableActivityType,
    TodoType, TodoItemType)


class SectionCreateUpdateMutation(graphene.Mutation):
    """
    Creates, updates and returns a `Section` object. \n
    To update all you need to do is pass in the section `id` as arguments.
    """
    section = graphene.Field(SectionType)
    success = graphene.Boolean()

    class Arguments:
        section_id = graphene.ID()
        name = graphene.String(
            description="""
            What name would you give this section.
            eg., '300Level Second Semester'""")
        description = graphene.String(description="""
            How will you describe this section,
            perhaps event what you hope to have accomplished
            at the end of this section""")
        start_date = graphene.Date(description="When does this section begin.")
        end_date = graphene.Date(description="When will this section end.")

    @classmethod
    @login_required
    def mutate(cls, root, info, **kwargs):
        section_id = kwargs.get("section_id", None)
        if section_id:
            try:
                section = Section.objects.get(pk=section_id)
            except Section.DoesNotExist:
                raise GraphQLError('Specified Section does not exist')
            if section.user == info.context.user:
                section.name = kwargs.get("name", section.name)
                section.description = kwargs.get(
                    "description", section.description)
                section.start_date = kwargs.get(
                    'start_date', section.start_date)
                section.end_date = kwargs.get('end_date', section.end_date)
                section.save()
                return SectionCreateUpdateMutation(
                    section=section, success=True)
            raise GraphQLError(
                'You do not have permissions to update this section')
        section = Section(
            user=info.context.user,
            name=kwargs.get('name', None),
            description=kwargs.get('description', None),
            start_date=kwargs.get('start_date', None),
            end_date=kwargs.get('end_date', None))
        section.save_base()
        return SectionCreateUpdateMutation(section=section, success=True)


class CourseCreateUpdateMutation(graphene.Mutation):
    """
    Creates, updates and returns a `Course` object.\n
    To update all you need to do is pass the course `id`.
    """
    course = graphene.Field(CourseType)
    success = graphene.Boolean()

    class Arguments:
        course_id = graphene.ID(
            description="""
            This is only required when performing an update to this section""")
        section_id = graphene.ID(
            description="""
            This is required if this course is for a specific section""")
        name = graphene.String(description="""
            What's the name of the course.""")
        description = graphene.String(description="""
            A short description of the course, perhaps it's purpose
            """)
        start_date = graphene.Date(description="""
            When will you start taking this course""")
        end_date = graphene.Date(description="""
            When will complete this course""")

    @classmethod
    @login_required
    def mutate(cls, root, info, **kwargs):
        section_id = kwargs.get('section_id', None)
        course_id = kwargs.get('course_id', None)
        section = None
        if section_id:
            try:
                section = Section.objects.get(pk=section_id)
                if section.user != info.context.user:
                    raise GraphQLError(
                        'You are not authorised to use this section')
            except Section.DoesNotExist:
                raise GraphQLError('Specified Section was not found')
        if course_id:
            try:
                course = Course.objects.get(pk=course_id)
                if course.user != info.context.user:
                    raise GraphQLError(
                        'You are not authorised to edit this course')
                course.name = kwargs.get('name', course.name)
                course.description = kwargs.get(
                    'description', course.description)
                course.start_date = kwargs.get('start_date', course.start_date)
                course.end_date = kwargs.get('end_date', course.end_date)
                course.section = section
                course.save()
                return CourseCreateUpdateMutation(course=course, success=True)
            except Course.DoesNotExist:
                raise GraphQLError('The specified course was not found')
        course = Course(
            name=kwargs.get('name', None),
            description=kwargs.get('description', None),
            end_date=kwargs.get('end_date', None),
            start_date=kwargs.get('start_date', None),
            section=section,
            user=info.context.user)
        course.save()
        return CourseCreateUpdateMutation(course=course, success=True)


class TopicCreateUpdateMutation(graphene.Mutation):
    """
    Creates, updates and returns a `Topic` object for a particular course.
    Note: a course `id` must be passed. \n
    To update, all you need to do is pass in the topic `id`.
    """
    topic = graphene.Field(TopicType)
    success = graphene.Boolean()

    class Arguments:
        name = graphene.String(
            description="What should this topic be called")
        description = graphene.String(
            description="A short summary of this topic")
        topic_id = graphene.ID(
            description="""
            This is only required when performing an update to the topic""")
        course_id = graphene.ID(
            required=True,
            description="The `id` of the course this topic belongs to.")

    @classmethod
    @login_required
    def mutate(cls, root, info, **kwargs):
        try:
            course = Course.objects.get(pk=kwargs.get('course_id'))
            if course.user != info.context.user:
                raise GraphQLError(
                    "You do not have permissions to use this course")
            topic_id = kwargs.get('topic_id', None)
            if topic_id:
                try:
                    topic = Topic.objects.get(pk=topic_id)
                    if topic.user != info.context.user:
                        raise GraphQLError(
                            'You do not have permissions to alter this topic')
                    topic.name = kwargs.get('name', topic.name)
                    topic.description = kwargs.get(
                        'description', topic.description)
                    topic.course = course
                    topic.user = info.context.user
                    topic.save()
                    return TopicCreateUpdateMutation(topic=topic, success=True)
                except Topic.DoesNotExist:
                    raise GraphQLError('The specified topic was not found')
            topic = Topic(
                name=kwargs.get('name', None),
                description=kwargs.get('description', None),
                course=course,
                user=info.context.user)
            topic.save()
            return TopicCreateUpdateMutation(topic=topic, success=True)
        except Course.DoesNotExist:
            raise GraphQLError('The specified course was not found')


class CreateUpdateResourceMuations(graphene.Mutation):
    """
    Creates or updates and returns a `Resource` object for a specific course.\n
    To update all you need to do is pass in the resource `id`.
    """
    resource = graphene.Field(ResourceType)
    success = graphene.Boolean()

    class Arguments:
        course_id = graphene.ID(
            required=True,
            description="`ID` for the course to which this resource belongs.")
        resource_id = graphene.ID(
            description="""The id of the target resource.\n
            Only pass this if you want to perform a update to a resource""")
        description = graphene.String(
            description="""\
            How would you describe this resource or what is it for""")
        document = Upload(
            required=False,
            description="upload document's here")
        link = graphene.String(
            description="Url to some resource on the internet.")
        audio = Upload(
            required=False,
            description="Audio resource like a lecture recording")
        video = Upload(
            required=False,
            description="Video resource, perhaps a lecture video recording")
        image = Upload(
            required=False,
            description="Images like a note snapshot etc go here")
        public = graphene.Boolean(
            description="""\
            Should this resource be made puplic and available to everyone.""")

    @classmethod
    @login_required
    def mutate(cls, root, info, **kwargs):
        course_id = kwargs.get('course_id', None)
        resource_id = kwargs.get('resource_id', None)

        if course_id:
            try:
                course = Course.objects.get(pk=course_id)
                if course.user != info.context.user:
                    raise GraphQLError(
                        'You do not have permissions to use this course')
                if resource_id:
                    try:
                        resource = Resource.objects.get(pk=resource_id)
                        resource.document = kwargs.get(
                            'document', resource.document)
                        resource.description = kwargs.get(
                            'description', resource.description)
                        resource.link = kwargs.get('link', resource.link)
                        resource.audio = kwargs.get(
                            'audio', resource.audio)
                        resource.video = kwargs.get(
                            'video', resource.video)
                        resource.image = kwargs.get(
                            'image', resource.image)
                        resource.puplic = kwargs.get(
                            'public', resource.public)
                        resource.course = course
                        resource.creator = info.context.user
                        resource.save()
                        return CreateUpdateResourceMuations(
                            resource=resource, success=True)
                    except Resource.DoesNotExist:
                        raise GraphQLError(
                            'The specified resource was not found')
                print('were here')
                resource = Resource.objects.create(
                    course=course,
                    creator=info.context.user,
                    description=kwargs.get('description', None),
                    link=kwargs.get('link', None),
                    public=kwargs.get('public', False),
                    document=kwargs.get('document', None),
                    audio=kwargs.get('audio', None),
                    video=kwargs.get('video', None),
                    image=kwargs.get('image', None))
                resource.save()
                print(resource)
                return CreateUpdateResourceMuations(
                    resource=resource, success=True)
            except Course.DoesNotExist:
                raise GraphQLError(
                    'Course with the specified `id` was not found')
        else:
            raise GraphQLError('Course `id` must be passed')


class TimeTableCreateUpdateMutation(graphene.Mutation):
    """
    Creates or updates and returns a `TimeTable` object.
    To update all you need to do is pass the time_table `id`.
    """
    time_table = graphene.Field(TimeTableType)
    success = graphene.Boolean()

    class Arguments:
        time_table_id = graphene.ID(description="""\
            If you want to perform an update, pass this""")
        section_id = graphene.ID(
            description="""\
                If this timetable is for a particular
                section then pass the section's `id`.""")
        course_id = graphene.ID(description="""\
                If this timetable is for a particular
                course then pass the course's `id`.""")
        topic_id = graphene.ID(description="""\
                If this timetable is for a particular
                topic then pass the topic's `id`.""")
        description = graphene.String(
            description="Describes what this timetable is for")
        public = graphene.Boolean(
            description="Should this time_table be made available to everyone")

    @classmethod
    @login_required
    def mutate(cls, root, info, **kwargs):
        section_id = kwargs.get('section_id', None)
        course_id = kwargs.get('course_id', None)
        topic_id = kwargs.get('topic_id', None)
        time_table_id = kwargs.get('time_table_id', None)
        try:
            section = Section.objects.get(
                pk=section_id) if section_id else None
            if section and section.user != info.context.user:
                raise GraphQLError('You are not permitted to use this section')
        except Section.DoesNotExist:
            raise GraphQLError('The specified section does not exist')

        try:
            course = Course.objects.get(pk=course_id) if course_id else None
            if course and course.user != info.context.user:
                raise GraphQLError('You are not permitted to use this course')
        except Course.DoesNotExist:
            raise GraphQLError('The specified course does not exist')

        try:
            topic = Topic.objects.get(pk=topic_id) if topic_id else None
            if topic and topic.user != info.context.user:
                raise GraphQLError('You are not permitted to use this topic')
        except Topic.DoesNotExist:
            raise GraphQLError('The specified topic does not exist')

        if time_table_id:
            try:
                t_table = TimeTable.objects.get(pk=time_table_id)
                if t_table.user != info.context.user:
                    raise GraphQLError(
                        'You are not permitted to alter this time_table')
                t_table.section = section if section_id else t_table.section
                t_table.course = course if course_id else t_table.course
                t_table.topic = topic if topic_id else t_table.topic
                t_table.description = kwargs.get(
                    'description', t_table.description)
                t_table.public = kwargs.get('public', t_table.public)
                t_table.user = info.context.user
                t_table.save()
                return TimeTableCreateUpdateMutation(
                    time_table=t_table, success=True)
            except TimeTable.DoesNotExist:
                raise GraphQLError('The specified time_table was not found')
        t_table = TimeTable(
            course=course,
            section=section,
            topic=topic,
            user=info.context.user,
            description=kwargs.get('description', None),
            public=kwargs.get('public', False))
        t_table.save()
        return TimeTableCreateUpdateMutation(
            time_table=t_table, success=True)


DaysOfTheWeekEnumSchema = graphene.Enum.from_enum(
    TimeTableActivity.DaysOfTheWeek)


class TimeTableActivityCreateUpdateMutation(graphene.Mutation):
    """
    Creates or updates and returns a `TimeTableActivity` object.
    If you want to perform an update, all you need to do is pass in
    the activity `id`.
    """
    activity = graphene.Field(TimeTableActivityType)
    success = graphene.Boolean()

    class Arguments:
        time_table_id = graphene.ID(
            required=True,
            description="""\
            The `id` of the time_table to which this activity belongs.""")
        activity_id = graphene.ID(
            description="""\
            The `id` of the time_table activity you wish to update""")
        start_time = graphene.Time(
            required=True,
            description="When does this activity begin")
        end_time = graphene.Time(
            required=True,
            description="When does this activity end")
        activity = graphene.String(
            required=True,
            description="The name of this activity")
        description = graphene.String('A description of this activity.')
        day = DaysOfTheWeekEnumSchema(
            required=True, description="Day for this activity")

    @classmethod
    @login_required
    def mutate(cls, root, info, **kwargs):
        time_table_id = kwargs.get('time_table_id', None)
        activity_id = kwargs.get('activity_id', None)
        if not time_table_id:
            raise GraphQLError('time_table_id is required')
        try:
            time_table = TimeTable.objects.get(pk=time_table_id)
            if time_table.user != info.context.user:
                raise GraphQLError(
                    'You are not permitted to use this time table')
            if activity_id:
                try:
                    activity = TimeTableActivity.objects.get(pk=activity_id)
                    if activity.user != info.context.user:
                        raise GraphQLError(
                            'You are not permitted to alter this activity')
                    activity.start_time = kwargs.get(
                        'start_time', activity.start_time)
                    activity.end_time = kwargs.get(
                        'end_time', activity.end_time)
                    activity.activity = kwargs.get(
                        'activity', activity.activity)
                    activity.description = kwargs.get(
                        'description', activity.description)
                    activity.day = kwargs.get('day', activity.day)
                    activity.timetable = time_table
                    activity.user = info.context.user
                    activity.save()
                    return TimeTableActivityCreateUpdateMutation(
                        activity=activity, success=True)
                except TimeTableActivity.DoesNotExist:
                    raise GraphQLError('The specified activity was not found')
            activity = TimeTableActivity(
                activity=kwargs.get('activity', None),
                start_time=kwargs.get('start_time', None),
                end_time=kwargs.get('end_time', None),
                day=kwargs.get('day', None),
                description=kwargs.get('description', None),
                timetable=time_table,
                user=info.context.user)
            activity.save()
            return TimeTableActivityCreateUpdateMutation(
                activity=activity, success=True)
        except TimeTable.DoesNotExist:
            raise GraphQLError('The specified time_table was not found')


class TodoListCreateUpdateMutation(graphene.Mutation):
    """
    Create or updates and return a `Todo` object.
    To update all you need to do is pass the todo `id`.
    """
    todo = graphene.Field(TodoType)
    success = True

    class Arguments:
        todo_id = graphene.ID(
            description="Pass this if you want to perform an update")
        name = graphene.String(
            required=True,
            description="What should this list be called")
        description = graphene.String(
            description="How would you describe this list or what is it for")
        public = graphene.Boolean(
            description="Should this list be made pulblic to everyone?")

    @classmethod
    @login_required
    def mutate(cls, root, info, **kwargs):
        todo_id = kwargs.get('todo_id', None)
        if todo_id:
            try:
                todo = Todo.objects.get(pk=todo_id)
                if todo.user != info.context.user:
                    raise GraphQLError(
                        'You are not permitted to alter this list')
                todo.name = kwargs.get('name', todo.name)
                todo.description = kwargs.get('description', todo.description)
                todo.public = kwargs.get('public', todo.public)
                todo.user = info.context.user
                todo.save()
                return TodoListCreateUpdateMutation(todo=todo, success=True)
            except Todo.DoesNotExist:
                raise GraphQLError('The specified todo_list was not found')
        todo = Todo(
            name=kwargs.get('name', None),
            description=kwargs.get('description', None),
            public=kwargs.get('public', False),
            user=info.context.user)
        todo.save()
        return TodoListCreateUpdateMutation(todo=todo, success=True)


class TodoItemCreateUpdateMutation(graphene.Mutation):
    """
    Creates or updates and returns a `TodoItem` object.\n
    To update all you need to do is pass the item `id`.
    """
    item = graphene.Field(TodoItemType)
    success = graphene.Boolean()

    class Arguments:
        todo_list_id = graphene.ID(
            required=True,
            description="`id` of the list to which this item belong.")
        item_id = graphene.ID(
            description="If you want to perform an update pass this.")
        start_time = graphene.Time(
            description="""\
            What time would you like to start this activity.
            Not required.""")
        end_time = graphene.Time(
            description="""
            When would you like to end this activity. Not required
            """)
        activity = graphene.String(
            description="What is this activity")
        description = graphene.String(
            description="What is this activity for.")
        day = graphene.Date(
            description="When do you plan to carry out this activity")

    @classmethod
    @login_required
    def mutate(cls, root, info, **kwargs):
        todo_list_id = kwargs.get('todo_list_id')
        item_id = kwargs.get('item_id', None)
        try:
            todo_list = Todo.objects.get(pk=todo_list_id)
            if todo_list.user != info.context.user:
                raise GraphQLError(
                    'You do not have permission to alter this list')
            if item_id:
                try:
                    item = TodoItem.objects.get(pk=item_id)
                    item.todo_list = todo_list
                    item.start_time = kwargs.get('start_time', item.start_time)
                    item.end_time = kwargs.get('end_time', item.end_time)
                    item.activity = kwargs.get('activity', item.activity)
                    item.description = kwargs.get(
                        'description', item.description)
                    item.day = kwargs.get('day', item.day)
                    item.save()
                    return TodoItemCreateUpdateMutation(
                        item=item, success=True)
                except TodoItem.DoesNotExist:
                    raise GraphQLError('The specified todo_item was not found')
            item = TodoItem(
                todo_list=todo_list,
                start_time=kwargs.get('start_time', None),
                end_time=kwargs.get('end_time', None),
                activity=kwargs.get('activity', None),
                description=kwargs.get('description', None),
                day=kwargs.get('day', None))
            item.save()
            return TodoItemCreateUpdateMutation(item=item, success=True)
        except Todo.DoesNotExist:
            raise GraphQLError('The specified todo_list was not found')


class TrackerMutation(graphene.ObjectType):
    create_update_section = SectionCreateUpdateMutation.Field()
    create_update_course = CourseCreateUpdateMutation.Field()
    create_update_topic = TopicCreateUpdateMutation.Field()
    create_update_resource = CreateUpdateResourceMuations.Field()
    create_update_time_table = TimeTableCreateUpdateMutation.Field()
    create_update_activity = TimeTableActivityCreateUpdateMutation.Field()
    create_update_todo_list = TodoListCreateUpdateMutation.Field()
    create_update_todo_item = TodoItemCreateUpdateMutation.Field()
