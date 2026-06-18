"""
    (1) SYSTEM DESIGN DOCUMENT
    1. Abstract Base Class - Equipment

    Equipment là lớp cha trừu tượng đại diện cho mọi trang bị trong game.

    Nhiệm vụ:

    Định nghĩa bộ khung chung cho tất cả item.
    Ép các class con phải có:
    calculate_total_damage()

    Ví dụ sau này thêm:

    class Bow(Equipment):

    nếu quên viết:

    calculate_total_damage()

    Python sẽ chặn ngay:

    TypeError:
    Can't instantiate abstract class Bow

    Thay vì để lỗi xảy ra lúc người chơi mở kho đồ.

    2. Multiple Inheritance & MRO

    MagicSword kế thừa:

    class MagicSword(Weapon, MagicMixin)

    MRO:

    MagicSword
            |
        Weapon
            |
        MagicMixin
            |
        Equipment
            |
        object

    Kiểm tra bằng:

    print(MagicSword.mro())
    Cách khởi tạo MagicSword

    Không được:

    super().__init__()

    một cách tùy tiện vì có thể bỏ sót magic_power.

    Thiết kế:

    class MagicSword(Weapon, MagicMixin):

        def __init__(self,...):

            Weapon.__init__(
                self,
                name,
                base_damage,
                upgrade_level
            )

            MagicMixin.__init__(
                self,
                magic_power
            )

    Kết quả:

    Object có đủ:

    name
    base_damage
    upgrade_level
    magic_power
    3. Polymorphism

    Kho đồ:

    inventory = [
        Weapon(),
        MagicSword()
    ]

    Duyệt:

    for item in inventory:

        item.calculate_total_damage()

    Python tự gọi:

    Weapon:

    base_damage + upgrade_level*10

    MagicSword:

    base_damage + upgrade_level*10 + magic_power

    Không cần:

    if type == Weapon
    elif type == MagicSword
    4. Operator Overloading
    add

    Pseudocode:

    function __add__(self, other):

        kiểm tra other có phải Equipment không

        nếu sai:
            trả về lỗi

        damage mới =
            damage weapon 1 + damage weapon 2

        level mới =
            upgrade_level1 + upgrade_level2

        tạo Weapon mới

        return Weapon mới

    Ví dụ:

    sword1 + sword2

    Python gọi:

    sword1.__add__(sword2)
"""

from abc import ABC, abstractmethod


# ==================================================
# ABSTRACT BASE CLASS
# ==================================================

class Equipment(ABC):
    """
    Lớp trừu tượng đại diện cho trang bị.
    """

    @abstractmethod
    def calculate_total_damage(self):
        """
        Tính sát thương tổng.
        """
        pass



# ==================================================
# WEAPON
# ==================================================

class Weapon(Equipment):
    """
    Vũ khí vật lý.
    """


    def __init__(self, name, base_damage, upgrade_level=0):

        self.name = name
        self.base_damage = base_damage
        self.upgrade_level = upgrade_level



    def calculate_total_damage(self):
        """
        Damage vật lý:
        base + level*10
        """

        return self.base_damage + self.upgrade_level * 10



    def __gt__(self, other):
        """
        So sánh sát thương.
        """

        if not isinstance(other, Equipment):

            print(
                "Chỉ có thể dung hợp/so sánh giữa các trang bị!"
            )

            return False


        return (
            self.calculate_total_damage()
            >
            other.calculate_total_damage()
        )



    def __add__(self, other):
        """
        Dung hợp 2 vũ khí.
        """

        if not isinstance(other, Equipment):

            print(
                "Chỉ có thể dung hợp/so sánh giữa các trang bị!"
            )

            return None



        new_name = (
            f"Fusion({self.name} + {other.name})"
        )


        new_damage = (
            self.base_damage
            +
            other.base_damage
        )


        new_level = (
            self.upgrade_level
            +
            other.upgrade_level
        )


        return Weapon(
            new_name,
            new_damage,
            new_level
        )



# ==================================================
# MAGIC MIXIN
# ==================================================

class MagicMixin:
    """
    Class hỗ trợ thuộc tính phép thuật.
    """


    def __init__(self, magic_power):

        self.magic_power = magic_power



    def cast_glow(self):

        print(
            f"{self.name} phát sáng bằng phép thuật!"
        )



# ==================================================
# MAGIC SWORD
# ==================================================

class MagicSword(Weapon, MagicMixin):
    """
    Kiếm ma thuật.
    Đa kế thừa Weapon + MagicMixin.
    """


    def __init__(
        self,
        name,
        base_damage,
        upgrade_level,
        magic_power
    ):


        Weapon.__init__(
            self,
            name,
            base_damage,
            upgrade_level
        )


        MagicMixin.__init__(
            self,
            magic_power
        )



    def calculate_total_damage(self):

        return (
            self.base_damage
            +
            self.upgrade_level * 10
            +
            self.magic_power
        )



# ==================================================
# INVENTORY
# ==================================================

inventory = []



def show_inventory():

    print(
        "\n--- KHO VŨ KHÍ CỦA NGƯỜI CHƠI ---"
    )


    if len(inventory) == 0:

        print(
            "Kho vũ khí hiện đang trống."
        )

        return



    for i,item in enumerate(
        inventory,
        start=1
    ):

        print(
            f"{i}. {item.name} | "
            f"{type(item).__name__} | "
            f"Level: {item.upgrade_level} | "
            f"Damage: {item.calculate_total_damage()}"
        )



# ==================================================
# CREATE WEAPON
# ==================================================

def create_weapon():

    print("\n--- RÈN VŨ KHÍ VẬT LÝ ---")


    name = input("Tên vũ khí: ")


    try:

        damage = int(
            input("Sát thương gốc: ")
        )


        level = int(
            input("Cấp cường hóa: ")
        )


        if damage <= 0 or level <= 0:

            print(
                "Giá trị phải lớn hơn 0!"
            )

            return



    except ValueError:

        print(
            "Dữ liệu không hợp lệ!"
        )

        return



    weapon = Weapon(
        name,
        damage,
        level
    )


    inventory.append(
        weapon
    )


    print(
        "Rèn Weapon thành công!"
    )



# ==================================================
# CREATE MAGIC SWORD
# ==================================================

def create_magic_sword():

    print(
        "\n--- RÈN KIẾM MA THUẬT ---"
    )


    name = input(
        "Tên kiếm ma thuật: "
    )


    try:

        damage = int(
            input("Sát thương gốc: ")
        )

        level = int(
            input("Cấp cường hóa: ")
        )

        magic = int(
            input("Sức mạnh phép thuật: ")
        )


        if (
            damage <=0
            or level <=0
            or magic <=0
        ):

            print(
                "Giá trị phải lớn hơn 0!"
            )

            return


    except ValueError:

        print(
            "Dữ liệu sai!"
        )

        return



    sword = MagicSword(
        name,
        damage,
        level,
        magic
    )


    inventory.append(
        sword
    )


    print(
        "Rèn MagicSword thành công!"
    )



# ==================================================
# COMPARE
# ==================================================

def compare_weapon():

    print(
        "\n--- THẨM ĐỊNH VŨ KHÍ ---"
    )


    if len(inventory)<2:

        print(
            "Cần ít nhất 2 vũ khí!"
        )

        return



    a = inventory[0]
    b = inventory[1]


    print(
        a.name,
        a.calculate_total_damage()
    )


    print(
        b.name,
        b.calculate_total_damage()
    )



    if a > b:

        print(
            f"{a.name} mạnh hơn {b.name}"
        )


    elif b > a:

        print(
            f"{b.name} mạnh hơn {a.name}"
        )


    else:

        print(
            "Hai vũ khí ngang sức!"
        )



# ==================================================
# FUSION
# ==================================================

def fusion_weapon():

    print(
        "\n--- DUNG HỢP VŨ KHÍ ---"
    )


    if len(inventory)<2:

        print(
            "Cần ít nhất 2 vũ khí!"
        )

        return



    new_weapon = (
        inventory[0]
        +
        inventory[1]
    )


    old1 = inventory.pop(0)

    old2 = inventory.pop(0)



    inventory.append(
        new_weapon
    )


    print(
        "Dung hợp thành công!"
    )


    print(
        "Vũ khí mới:",
        new_weapon.name
    )


    print(
        "Damage:",
        new_weapon.calculate_total_damage()
    )



# ==================================================
# MAIN MENU
# ==================================================

while True:


    print("""
===== LÒ RÈN VŨ KHÍ RIKKEI STUDIOS =====

1. Xem kho vũ khí
2. Rèn Weapon
3. Rèn MagicSword
4. Thẩm định
5. Dung hợp
6. Thoát

""")


    choice = input(
        "Chọn chức năng: "
    )



    if choice=="1":

        show_inventory()


    elif choice=="2":

        create_weapon()


    elif choice=="3":

        create_magic_sword()


    elif choice=="4":

        compare_weapon()


    elif choice=="5":

        fusion_weapon()


    elif choice=="6":

        print(
            "Thoát Lò Rèn. Hẹn gặp lại Anh hùng!"
        )

        break


    else:

        print(
            "Lựa chọn không hợp lệ!"
        )