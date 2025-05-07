// generated file, do not edit
{% for t in tfs %}
{% if t.badge_type == "misc" %}
import {{ t.name }}_image from "@image/{{ t.badge_path }}"
{% endif %}
{% endfor %}

const template = "https://upload-bbs.mihoyo.com/game_record/genshin/character_icon/#.png"
const newTemplate = "https://act-webstatic.mihoyo.com/hk4e/e20200928calculate/item_icon_u9b0pg/#.png"
const getImage = name => template.replace("#", name)
const getIcon = hash => newTemplate.replace("#", hash)

export default {
    {% for t in tfs %}
    "{{ t.name }}": {
        name: "{{ t.name }}",
        nameLocale: {{t.name_locale}},
        description: {{t.description}},
        tags: [
            {% for tag in t.tags %}
            "{{ tag }}",
            {% endfor %}
        ],
        "for": "{{ t.four }}",
        {% if t.badge_type == "character" && t.icon_hash == "" -%}
        badge: getImage("{{ t.character_icon_name }}"),
        {%- else if t.badge_type == "character" -%}
        badge: getIcon("{{ t.icon_hash }}"),
        {%- else -%}
        badge: {{ t.name }}_image,
        {%- endif %}
        config: [
            {% for config in t.config %}
            {{ config|e("none") }},
            {% endfor %}
        ],
    },
    {% endfor %}
}
