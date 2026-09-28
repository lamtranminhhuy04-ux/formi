# Kiểm tra font tiếng Việt và theme hồng pastel

Ngày: 11/09/2026. Dự án: `D:/FPT/Web/formi`. Trình duyệt: Microsoft Edge Chromium trên Windows, chạy headless bằng Playwright. Không thêm dependency vào website và không thay đổi `js/data.js`.

## 1. Nguyên nhân gốc

- `<meta charset="utf-8">` ở byte 42, đúng và đủ sớm.
- HTML, CSS, JavaScript giải mã UTF-8 nghiêm ngặt thành công; không tìm thấy ký tự thay thế hoặc mẫu mojibake đã kiểm tra. Nội dung là NFC.
- CSS cũ dùng Georgia cho tiêu đề/chữ nghiêng, Segoe UI cho nội dung; một số shorthand trong caption/chữ ký/footer khai báo lại stack.
- `georgia.ttf` và `georgiai.ttf` trên máy thiếu 49 ký tự chữ cái xuất hiện trong `data.js`. Có trường hợp trình duyệt dựng dấu bằng glyph tổ hợp, có trường hợp rơi xuống font kế tiếp.
- Bằng chứng CDP trước sửa: `#reason-title` dùng Georgia (30 glyph) **và Times New Roman (3 glyph)**; `#hero-caption` dùng Georgia Italic (37) và Times New Roman Italic (3); `#signature` dùng Georgia Italic (13) và Times New Roman Italic (2).
- Không có font CDN/@font-face bị tải lỗi ở phiên bản cũ, vì chưa dùng web font. `font-weight:650` của nhãn dùng Segoe UI Bold trên máy này; không phải weight tải riêng.

**Kết luận:** lỗi chính là thiếu glyph và font fallback xen kẽ, không phải dữ liệu sai encoding. Vì vậy không sửa/bỏ dấu tiếng Việt trong nội dung.

## 2. Cách sửa font

- Nội dung/nút: Noto Sans variable 400–700.
- Tiêu đề/chữ ký/điểm nhấn: Lora subset normal 400 và italic 400 thật, đổi tên thành **Universe Serif** để tôn trọng Reserved Font Name của giấy phép SIL OFL 1.1.
- Ba file WOFF2 cục bộ tổng 141.468 byte, kèm giấy phép, nguồn và SHA-256 trong `assets/fonts/`. Có `font-display: swap`, preload hai file dùng ngay đầu trang.
- Kiểm tra `cmap` bao gồm toàn dải chữ Việt U+1EA0–U+1EF9, các nguyên âm có dấu, Đ/đ và dấu tổ hợp NFD. Không thiếu glyph trong tập kiểm tra.
- Kiểm tra font render thực tế: từng nhóm nội dung dùng một font cục bộ, không trộn Georgia/Times. Probe 400/600/650/700, normal/italic và NFC/NFD đều dùng một web font cho chữ tiếng Việt.
- Khi chặn tất cả WOFF2, nội dung vẫn đọc được bằng font hệ thống; trên máy này có Noto Sans hệ thống và Times New Roman. Kiểm tra thêm trực tiếp `cmap` của Segoe UI/Arial/Times cho tập tiếng Việt thành công.
- Đã tăng khoảng dòng cho điểm nhấn và nâng một số nhãn quá nhỏ trên mobile. Không dùng font viết tay thiếu glyph hoặc giả lập italic.

## 3. Theme hồng pastel

Toàn bộ màu UI chuyển về CSS custom properties trong `:root`: nền `#FFF7FA`, section `#FCEEF3`, card `#FFFDFC`, pastel `#E8A8B8`, accent `#D97993`, nút/focus `#9D4E67`, chữ `#4A3038`, chữ phụ `#76545F`, border `#EBCDD6`.

Đồng bộ header, hero, timeline, map/pin, Polaroid, quiz, envelope, letter, countdown, gift, dialog, lightbox, disabled/hover/active/focus và confetti. Giữ texture, góc nghiêng, băng dính, tem và nhiều lớp giấy. Tất cả mã màu CSS UI được gom vào root; không còn palette nâu/olive cũ trong selector.

SVG bản đồ và nền ảnh mẫu đã phối lại. Màu da/tóc, cây cỏ, bánh và vật thể tự nhiên trong các cảnh được giữ có chủ đích; không áp filter lên ảnh người dùng.

## 4. File thêm hoặc thay đổi trong đợt này

| File/nhóm | Thay đổi |
| --- | --- |
| `index.html` | Theme-color, font stylesheet, preload WOFF2 |
| `css/fonts.css` | Ba khai báo font face chính xác style/weight |
| `css/styles.css` | Theme token, font stack, responsive typography, focus/disabled, định dạng lại CSS để dễ bảo trì |
| `assets/fonts/` | 3 WOFF2, 2 OFL, README nguồn, manifest hash |
| `assets/icons/star.svg` | Favicon pastel |
| `assets/images/{hero-placeholder,map-placeholder,photo-placeholder,cafe,mountains,flowers,picnic,night}.svg` | Phối lại màu cảnh mẫu |
| `js/app.js` | Đồng bộ storage, map fallback, trạng thái lỗi audio, timer và màu confetti |
| `js/quiz.js` | Tiến trình sau đáp án, cập nhật khi tab khác hoàn thành/reset |
| `tests/browser_check.py` | Giữ 59 kiểm tra; chờ font tải trước chụp ảnh |
| `tests/font_probe.py` | Bằng chứng glyph/font render và ảnh chữ trước/sau |
| `tests/theme_check.py` | 196 kiểm tra bổ sung |
| `README.md`, `QA-REPORT.md`, `docs/qa/` | Hướng dẫn, kết quả và ảnh desktop/mobile |

Giữ nguyên 12 bước hành trình, nội dung, cấu trúc `data.js`, các đường dẫn tương đối, `.nojekyll` và cơ chế mở quà cần đủ quiz + ngày hẹn. Không commit/push/deploy thay người dùng.

## 5. Lỗi khác đã sửa

| Vấn đề có bằng chứng | Sửa và xác minh |
| --- | --- |
| Mở thư A ở tab 1, thư B ở tab 2 chỉ còn `openedLetters:["miss"]` | Hợp nhất trạng thái trước khi lưu, đồng bộ dấu đã đọc giữa tab; test giữ cả `sad` và `miss` |
| Tab khác nhận khóa quiz nhưng UI vẫn hiển thị câu hỏi cũ; reset không cập nhật | Làm mới UI quiz và điều kiện quà khi nhận storage event; kiểm tra cả hoàn thành và reset |
| File nhạc 404: Promise catch/`pause` có thể ghi đè nhãn lỗi thành “Bật nhạc” | Giữ cờ lỗi audio; test xác nhận nút disabled vẫn ghi “Nhạc chưa khả dụng” |
| Đường dẫn bản đồ tùy chỉnh sai chưa có fallback | Dùng map-placeholder cục bộ khi ảnh lỗi; ghim vẫn hoạt động |
| Thanh tiến trình chưa tăng ngay sau khi trả lời | Tăng sau khi chọn đáp án, trước nút câu tiếp theo |

Cải thiện nhỏ: timer tạm dừng khi tab ẩn/pagehide, khởi động lại khi quay lại; không tạo thêm interval trùng. Card nội dung trên mobile được ưu tiên một cột để tăng độ dễ đọc.

## 6. Kiểm thử trước và sau

| Bộ kiểm tra | Trước | Sau |
| --- | --- | --- |
| Bộ chức năng hiện có | 59/59 | 59/59 |
| Bộ bổ sung font/theme/network/mobile/accessibility | Chưa có | 196/196 |
| Cú pháp 5 file JavaScript | Hợp lệ | Hợp lệ |
| HTML5 parser, CSS parser, SVG XML | Kiểm tra ở đợt này | Không lỗi parser |
| Chữ Việt ở tiêu đề/caption | Trộn Georgia/Times | Một font cục bộ cho mỗi kiểu chữ |

196 là số assertion (bao gồm kiểm tra đường dẫn/từng kích thước), không phải 196 kịch bản độc lập. Các kiểm tra chạy trong browser context tách biệt, không xóa localStorage của người dùng. Test audio chỉ dùng WAV sinh trong bộ nhớ; test cấu hình không sửa `data.js` trên đĩa.

## 7. Responsive và accessibility

| Viewport | Tràn ngang | Modal/lightbox | Vùng bấm chính ≥44px | Thư cuối |
| --- | --- | --- | --- | --- |
| 320×812 | Không | Đạt | Đạt | Đọc được, không tràn |
| 375×812 | Không | Đạt | Đạt | Đọc được, không tràn |
| 768×1024 | Không | Đạt | Đạt | Đọc được, không tràn |
| 1024×768 | Không | Đạt | Đạt | Đọc được, không tràn |
| 1440×960 | Không | Đạt | Đạt | Đọc được, không tràn |
| 812×375 (ngang) | Không | Đạt | Đạt | Đọc được, không tràn |

Đã kiểm tra headings/landmarks, ID duy nhất, link nội trang, accessible name, alt, Tab/Shift+Tab/Escape, khôi phục focus, phím mũi tên, reduced motion, phản hồi quiz bằng chữ/ký hiệu và countdown không aria-live mỗi giây. Font fallback bị chặn vẫn dùng được trên mobile.

Tỷ lệ tương phản màu solid (WCAG):

| Cặp màu | Tỷ lệ |
| --- | --- |
| Chữ chính / nền | 11,26:1 |
| Chữ phụ / nền | 6,22:1 |
| Chữ phụ / section | 5,83:1 |
| Chữ trên nút / nút chính | 5,57:1 |
| Chữ phụ / phong bì | 4,59:1 |
| Chữ disabled / nền disabled | 5,12:1 |

Các cặp kiểm tra đều đạt AA cho chữ thường; focus đạt trên 3:1. Đây không phải chứng nhận WCAG toàn diện, đặc biệt với ảnh hoặc nội dung người dùng thay sau này.

## 8. Console, network, asset và hiệu năng

- Phiên bình thường: 0 JavaScript error, 0 console error/warning, 0 failed request/404. 21 response được ghi nhận, đều dưới subpath dự án; không request CDN/API.
- Chạy được bằng `file://`, server ở root, server dưới subpath. Kiểm tra từng đoạn tên đường dẫn có đúng chữ hoa/thường.
- Mô phỏng riêng: chặn font; audio 404; bản đồ 404. Các lỗi network ở ba tình huống này là chủ đích và có fallback, không tính là phiên bình thường.
- Ảnh minh họa tổng khoảng 11,7KB; font 138KiB. Encoded resource bodies trong phiên đo khoảng 212KB, chưa bao gồm tài nguyên bạn thêm sau này.
- CLS lúc tải trang trong một lần đo local: khoảng **0,0024**. Không phải kết quả mạng di động/CPU yếu hoặc Lighthouse thực địa.
- Lazy images có kích thước định trước; lightbox không preload toàn album; audio preload none; confetti dọn khỏi DOM sau hiệu ứng. Giảm chuyển động bỏ animation và confetti.

## 9. Đề xuất cải thiện

**Cần làm ngay:** các lỗi đã tái hiện trong phạm vi này đã sửa; chưa còn lỗi chặn chức năng nào được phát hiện qua các phép kiểm tra đã chạy.

**Nên cải thiện:** thử trên iPhone/Safari, Android và screen reader thật trước khi tặng; kiểm tra lại tương phản/khung ảnh khi thay ảnh cá nhân. Giữ ảnh nén hợp lý và giấy phép font khi deploy. Không tự thêm dependency hoặc bước build.

**Tùy chọn:** ảnh thật có crop riêng cho hero/timeline, nhạc cá nhân hợp pháp, hoặc một hình thức quà khác như video/playlist. Chưa tự triển khai các tính năng mở rộng.

## 10. Giới hạn

Chưa kiểm tra thiết bị vật lý, Safari/Firefox hoặc VoiceOver/TalkBack/NVDA. Chưa deploy lên GitHub thật do chưa có yêu cầu xuất bản/repository đích. Chỉ mô phỏng project subpath bằng server cục bộ và kiểm tra đường dẫn. Không có video/playlist/QR nhúng trong bản hiện tại: quà là ảnh và lời mời cục bộ, vì vậy không tuyên bố đã kiểm tra trình phát bên ngoài. WAV thử chứng minh play/pause/error handling, không thay thế thử codec/tệp nhạc thật của bạn.

## 11. Cách tự kiểm tra

1. Mở `index.html`, hard-refresh nếu trình duyệt còn cache bản cũ. Xem tên hai người, chữ ký và tiêu đề có dấu.
2. Thu hẹp màn hình xuống 320/375px; mở ghim, album, thư và làm quiz.
3. Dùng Tab, Shift+Tab, Escape và mũi tên trong lightbox.
4. Mở hai tab cùng URL; đọc hai thư khác nhau, tải lại để xác nhận cả hai vẫn được đánh dấu.
5. Khi thử quà, dùng `bypassCountdown` như README hướng dẫn rồi trả về `false`. Không thay đổi ngày thật nếu không cần thiết.
6. Chạy `python tests/browser_check.py` và `python tests/theme_check.py` sau khi cài công cụ QA tùy chọn theo README.

## 12. Ảnh và bằng chứng

- [Desktop](docs/qa/desktop.png)
- [Mobile](docs/qa/mobile.png)
- [Probe tiếng Việt sau sửa](docs/qa/vietnamese-fonts.png)
- Bằng chứng chi tiết được tái tạo tại `tests/artifacts/`: `audit-before.json`, `audit-after.json`, `theme-results.json`, `results.json`, ảnh full page của 5 độ rộng. Thư mục artifacts được gitignore để không đưa toàn bộ dữ liệu test lên Pages.
