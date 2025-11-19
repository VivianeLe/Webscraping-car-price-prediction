from pydantic import BaseModel, root_validator
from enum import Enum
import csv
import pathlib
import re
from typing import Dict, List, Optional, Tuple

# ===== 1) Load (Brand, Name, Color) từ CSV =====
def load_brand_name_pairs(csv_path: pathlib.Path) -> List[Tuple[str, str, str]]:
    pairs: List[Tuple[str, str, str]] = []
    try:
        with open(csv_path, newline='', encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                brand = (row.get("Brand") or "").strip()
                name = (row.get("Name") or "").strip()
                color = (row.get("Color") or "").strip()
                # Chỉ cần brand & name; color có thể rỗng (tùy dữ liệu)
                if brand and name:
                    pairs.append((brand, name, color))
    except Exception:
        # In production: log lỗi nếu cần
        pass
    # Loại trùng và sắp xếp ổn định
    pairs = sorted(set(pairs))
    return pairs

# ===== 2) Tạo Enum động từ bộ (Brand, Name, Color) =====
_sep = "__"  # separator an toàn để ghép value

def sanitize_member_name(s: str) -> str:
    """
    Biến chuỗi thành tên hằng Enum hợp lệ:
    - bỏ '_' ở 2 đầu
    """
    return s.strip('_')

def build_brand_name_enum(pairs: List[Tuple[str, str, str]]) -> Enum:
    """
    Tạo Enum 'BrandNameOption', mỗi member có value là chuỗi 'Brand__Name__Color'.
    Đưa cả Color vào tên member để tránh trùng trong trường hợp cùng 
    Brand/Name nhưng khác Color.
    """
    members: Dict[str, str] = {}
    seen_member_names = set()

    for brand, name, color in pairs:
        # Value giữ nguyên để tách ngược lại dễ dàng
        value = f"{brand}{_sep}{name}{_sep}{color}"
        member = f"{sanitize_member_name(brand)}__{sanitize_member_name(name)}__{sanitize_member_name(color)}"
        seen_member_names.add(member)
        members[member] = value

    return Enum("BrandNameOption", members)  # type: ignore

# CSV path
BRAND_NAME_CSV = pathlib.Path(__file__).parent.parent.parent / "data" / "brand_name_color_pairs.csv"

# Build enum ngay khi import
_brand_name_pairs = load_brand_name_pairs(BRAND_NAME_CSV)
BrandNameOption = build_brand_name_enum(_brand_name_pairs)

# ===== 3) Request model: người dùng CHỈ chọn 1 trường brand_name_color =====
class CarPriceRequest(BaseModel):
    # User phải chọn đúng 1 option trong enum này (limit input hợp lệ)
    # brand_name_color: BrandNameOption
    Brand: str
    Name: str
    Color: str
    Fuel: str
    Gearbox: str
    Year: int
    Km: int
    Fuel_consumption: float
    Co2_emission: float
    Doors: float

    # 3 trường này sẽ được *suy ra* từ brand_name_color, không cho user nhập tay
    # Brand: Optional[str] = None
    # Name: Optional[str] = None
    # Color: Optional[str] = None

    # @root_validator(pre=False, skip_on_failure=True)
    # def populate_brand_name_color(cls, values):
    #     """
    #     Sau khi validate, tách Brand/Name/Color từ brand_name_color.value ('Brand__Name__Color')
    #     và gán vào 3 field Brand/Name/Color để dùng downstream.
    #     """
    #     bn: BrandNameOption = values.get("brand_name_color")  # type: ignore
    #     if bn is not None:
    #         parts = bn.value.split(_sep)
    #         # Đảm bảo luôn có đủ 3 phần (Color có thể rỗng string)
    #         if len(parts) == 3:
    #             brand, name, color = parts
    #         else:
    #             # fallback an toàn (ít gặp)
    #             brand, name, color = (parts + ["", ""])[:3]
    #         values["Brand"] = brand
    #         values["Name"] = name
    #         values["Color"] = color
    #     return values
