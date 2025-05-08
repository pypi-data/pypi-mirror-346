from constance import config
from django import template
from django.conf import settings
from django.templatetags.static import static
from django.utils.safestring import mark_safe

register = template.Library()

v3_site_key = getattr(settings, "RECAPTCHA_V3_SITE_KEY", "")
v3_secret_key = getattr(settings, "RECAPTCHA_V3_SECRET_KEY", "")
v2_site_key = getattr(settings, "RECAPTCHA_V2_SITE_KEY", "")
v2_secret_key = getattr(settings, "RECAPTCHA_V2_SECRET_KEY", "")
vue_recaptcha_url = static("vendor/vue-recaptcha/vue-recaptcha.min.js")


@register.simple_tag
def RECAPTCHA_UPPER_SCORE():
    return config.GOOGLE_RECAPTCHA_V3_UPPER_SCORE


@register.simple_tag
def RECAPTCHA_LOWER_SCORE():
    return config.GOOGLE_RECAPTCHA_V3_LOWER_SCORE


@register.simple_tag
def RECAPTCHA_V3_SITE_KEY():
    return v3_site_key


@register.simple_tag
def RECAPTCHA_V3_SECRET_KEY():
    return v3_secret_key


@register.simple_tag
def RECAPTCHA_V2_SITE_KEY():
    return v2_site_key


@register.simple_tag
def RECAPTCHA_V2_SECRET_KEY():
    return v2_secret_key


@register.simple_tag
def RECAPTCHA_SCRIPTS_INCLUDE():
    html = f'<script src="https://www.google.com/recaptcha/api.js?render={v3_site_key}"></script>'
    html += '<script src="https://www.google.com/recaptcha/api.js?onload=vueRecaptchaApiLoaded&render=explicit" async defer></script>'
    html += f'<script src="{vue_recaptcha_url}"></script>'
    html += "<style>.grecaptcha-badge {{ opacity:0;}}</style>"
    return mark_safe(html)  # nosemgrep


@register.simple_tag
def RECAPTCHA_SCRIPT():
    html = (
        f"grecaptcha.ready(function () {{"
        f"grecaptcha.execute('{v3_site_key}', {{ action: 'load' }}).then(function (token) {{"
        f'axios.post("/api/services/google/re_captcha",'
        f"                  {{response: token}}"
        f"                  ).then(function (response) {{"
        f"            let score= response.data.data.score;"
        f"            vm.score= score;"
        f"            if(score > {RECAPTCHA_UPPER_SCORE()}){{"
        f"              vm.showv2= false;"
        f"            }}else if({RECAPTCHA_UPPER_SCORE()} >= score > {RECAPTCHA_LOWER_SCORE()}){{"
        f"              vm.showv2= true;"
        f"            }}else{{"
        f"              vm.showv2= true;"
        f"            }}"
        f"          }}).catch(function (error) {{"
        f"              vm.showv2= true;"
        f"          }});"
        f"        }});"
        f"      }});   "
    )

    return mark_safe(html)  # nosemgrep
