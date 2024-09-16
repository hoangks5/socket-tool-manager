class DescriptionGroupBox:
    def __init__(self, ui):
        """Initialize the DescriptionGroupBox with a UI reference."""
        super().__init__()
        self.ui = ui
        self.set_tooltips()

    def set_tooltips(self):
        """Set tooltips for various UI elements in the application with HTML formatting."""

        # Browser Section
        self.ui.chrome_6.setToolTip("Tạo <b>chrome</b> mới để chạy")

        # Keyboard Section
        self.ui.click_15.setToolTip("Gõ một đoạn văn bản như một <b>người dùng</b>")
        self.ui.click_16.setToolTip(
            "Thực hiện một phím bấm<br>"
            "Nhập phím vào ô text hoặc bấm nút <b>Get</b> để chọn phím"
        )
        self.ui.click_19.setToolTip(
            "Thực hiện chuỗi phím bấm<br>"
            "Nhập chuỗi phím vào ô text, mỗi phím cách nhau bởi dấu cách<br>"
            "Bấm nút <b>Get</b> để chọn chuỗi phím cần bấm"
        )

        # Mouse Section
        self.ui.click_17.setToolTip(
            "Di chuyển chuột đến một tọa độ (x, y)<br>"
            "Nhập tọa độ <b>x</b>, <b>y</b> hoặc bấm <b>Get</b> để chọn điểm di chuyển và click để lấy tọa độ"
        )
        self.ui.click_20.setToolTip(
            "Di chuyển chuột đến một điểm ngẫu nhiên trong vùng<br>"
            "Nhập tọa độ <b>x</b>, <b>y</b>, <b>width</b>, <b>height</b> hoặc bấm <b>Get</b> để chọn vùng di chuyển"
        )
        self.ui.sleep_14.setToolTip(
            "Click chuột <b>trái</b> hoặc <b>phải</b><br>"
            "H.Left hoặc H.Right để giữ và click chuột <b>trái</b> hoặc <b>phải</b>"
        )
        self.ui.click_18.setToolTip("Scroll chuột lên hoặc xuống")

        # AI Section
        self.ui.click_24.setToolTip(
            "Nhận diện hình ảnh và di chuyển chuột đến vị trí hình ảnh<br>"
            "Bấm <b>Crop</b> để cắt hình ảnh<br>"
            "Bấm <b>Paste</b> để dán mã base64 của hình ảnh vào ô text"
        )
