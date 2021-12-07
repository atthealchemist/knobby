from pathlib import Path

import attr
import pytest
from PIL import Image

from constants import DATA_DIR
from modules.builders import KnobStripBuilder, StripBuilder
from modules.entities import KnobRotation, StripDirection

test_knob_file_path = f"{DATA_DIR}/knob.png"
test_led_file_paths = [
    f"{DATA_DIR}/led_off.png",
    f"{DATA_DIR}/led_on.png",
]
test_result_file_path = f"{DATA_DIR}/test_led_horizontal.png"


@pytest.fixture
def led_images():
    """
    Фикстура создаёт набор тестовых изображений (объекты PIL.Image)
    из путей тестовых файлов с изображением включенного светодиода
    (led_on) и выключенного светодиода (led_off).
    """
    return [Image.open(led_path) for led_path in test_led_file_paths]


@pytest.fixture
def test_knob_image():
    """
    Фикстура создаёт тестовое изображение (объект PIL.Image)
    из пути тестового файла с изображением ручки (knob).
    """
    return Image.open(test_knob_file_path)


def test_strip_builder(led_images):
    """
    Тестируется создание и сохранение стрипа.
    """
    test_strip_direction = "horizontal"
    sb = StripBuilder(images=led_images, direction=test_strip_direction)
    res = sb.build()
    res.save(file_path=test_result_file_path)
    assert res.strip.direction.value == test_strip_direction
    assert attr.asdict(res.metadata) == {
        "file_paths": test_led_file_paths,
        "frames_count": 2,
        "extra": {},
    }
    assert Path(test_result_file_path).is_file()


def test_knob_strip_builder(test_knob_image):
    """
    Тестируется создание и сохранение кноб стрипа.
    """
    sb = KnobStripBuilder(
        knob_image=test_knob_image,
        direction="vertical",
        rotation="clockwise",
    )
    res = sb.build()
    res.save(file_path=test_result_file_path)
    assert res.strip.direction == StripDirection.VERTICAL
    assert attr.asdict(res.metadata) == {
        "extra": {"rotation": KnobRotation.CLOCKWISE},
        "file_paths": [test_knob_file_path],
        "frames_count": 27,
    }
    assert Path(test_result_file_path).is_file()
