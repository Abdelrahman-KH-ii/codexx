# -*- coding: utf-8 -*-
from django import template
from courses.translation_dict import (
    COURSE_TRANSLATIONS,
    CATEGORIES_AR,
    STACKS_AR,
    DIFFICULTIES_AR,
)

register = template.Library()

@register.filter
def translate_title(course, lang):
    if lang == 'ar':
        trans = COURSE_TRANSLATIONS.get(course.slug)
        if trans and 'title' in trans:
            return trans['title']
    return course.title

@register.filter
def translate_short(course, lang):
    if lang == 'ar':
        trans = COURSE_TRANSLATIONS.get(course.slug)
        if trans and 'short' in trans:
            return trans['short']
    return course.short_description

@register.filter
def translate_category(course, lang):
    if lang == 'ar':
        return CATEGORIES_AR.get(course.category, course.category_label)
    return course.category_label

@register.filter
def translate_stack(course, lang):
    if lang == 'ar':
        return STACKS_AR.get(course.stack, course.stack_label)
    return course.stack_label

@register.filter
def translate_difficulty(course, lang):
    if lang == 'ar':
        return DIFFICULTIES_AR.get(course.difficulty, course.get_difficulty_display())
    return course.get_difficulty_display()
