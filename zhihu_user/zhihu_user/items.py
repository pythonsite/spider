# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Item,Field


class UserItem(scrapy.Item):
    id = Field()
    name = Field()
    account_status = Field()
    allow_message= Field()
    answer_count = Field()
    articles_count = Field()
    avatar_hue = Field()
    avatar_url = Field()
    avatar_url_template = Field()
    badge = Field()
    business = Field()
    employments = Field()
    columns_count = Field()
    commercial_question_count = Field()
    cover_url = Field()
    description = Field()
    educations = Field()
    favorite_count = Field()
    favorited_count = Field()
    follower_count = Field()
    following_columns_count = Field()
    following_favlists_count = Field()
    following_question_count = Field()
    following_topic_count = Field()
    gender = Field()
    headline = Field()
    hosted_live_count = Field()
    is_active = Field()
    is_bind_sina = Field()
    is_blocked = Field()
    is_advertiser = Field()
    is_blocking = Field()
    is_followed = Field()
    is_following = Field()
    is_force_renamed = Field()
    is_privacy_protected = Field()
    locations = Field()
    is_org = Field()
    type = Field()
    url = Field()
    url_token = Field()
    user_type = Field()
    logs_count = Field()
    marked_answers_count = Field()
    marked_answers_text = Field()
    message_thread_token = Field()
    mutual_followees_count = Field()
    participated_live_count = Field()
    pins_count = Field()
    question_count = Field()
    show_sina_weibo = Field()
    thank_from_count = Field()
    thank_to_count = Field()
    thanked_count = Field()
    type = Field()
    vote_from_count = Field()
    vote_to_count = Field()
    voteup_count = Field()



