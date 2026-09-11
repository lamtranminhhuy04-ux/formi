# Our Little Universe

Một cuốn scrapbook tình yêu bằng **HTML, CSS và JavaScript thuần**, chạy ngay khi mở `index.html`. Không framework, npm, bundler, backend, database, API key hay dịch vụ trả phí. Tất cả ảnh mẫu đều là SVG cục bộ; không cần mạng để tải font hoặc ảnh.

## Chạy website

Mở `index.html` bằng Edge, Chrome, Firefox hoặc Safari phiên bản hiện đại. JavaScript cần được bật. Không phải cài đặt gì.

Nếu muốn dùng static server, mở terminal tại thư mục dự án:

```sh
python -m http.server 8000
```

Mở `http://localhost:8000`. Python chỉ là công cụ xem thử tùy chọn, website không phụ thuộc vào server này. Nhấn `Ctrl+C` để dừng. Trạng thái `localStorage` riêng theo trình duyệt và origin; mở bằng file và mở qua server có thể có tiến độ khác nhau.

## Nội dung và cấu trúc

| Đường dẫn | Vai trò |
| --- | --- |
| `index.html` | 12 phần theo thứ tự hành trình, điều hướng và dialog |
| `css/reset.css` | Thiết lập CSS cơ bản |
| `css/styles.css` | Màu, bố cục, responsive, chuyển động, focus |
| `js/data.js` | **Tất cả nội dung cá nhân cần thay** |
| `js/app.js` | Render, bản đồ, thư, âm thanh, trạng thái quà |
| `js/countdown.js` | Tính thời gian và xử lý ngày không hợp lệ |
| `js/quiz.js` | Câu hỏi, phản hồi, kết quả, chơi lại |
| `js/gallery.js` | Album, lightbox, phím mũi tên |
| `assets/images/` | Hero, bản đồ, 5 cảnh minh họa, ảnh dự phòng và texture giấy |
| `assets/icons/star.svg` | Favicon |
| `assets/audio/README.md` | Cách thêm nhạc thật |
| `.nojekyll` | Phục vụ website tĩnh trên GitHub Pages |
| `tests/browser_check.py` | Kiểm tra trình duyệt tùy chọn cho người bảo trì |

Hành trình: chào → số ngày bên nhau → lời mở đầu → 6 cột mốc → bản đồ → 6 ảnh Polaroid → 5 điều yêu → 5 câu quiz → 4 thư “Open when” → thư cuối → countdown → quà.

## Cá nhân hóa trong `js/data.js`

**Mây, Nắng, toàn bộ ngày tháng, câu chuyện và hình ảnh hiện tại đều là dữ liệu mẫu**, không phải thông tin cá nhân thật. Thay dữ liệu trước khi gửi tặng. Giữ dấu phẩy, ngoặc và dấu nháy như ví dụ. Có thể dùng `\n` bên trong chuỗi để xuống dòng; các đoạn thư dài dùng nhiều chuỗi trong một mảng.

| Muốn thay | Trường cần sửa |
| --- | --- |
| Tên website | `siteName` |
| Tên/biệt danh hai người | `names: ["Tên người thứ nhất", "Tên người thứ hai"]` |
| Ngày bắt đầu yêu | `startDate` |
| Ngày mở quà | `targetDate` và câu mô tả `countdownCaption` |
| Múi giờ trình bày | `timeZone` (mặc định `Asia/Ho_Chi_Minh`) |
| Lời chào, ảnh hero | `intro`, `heroImage`, `heroAlt`, `heroCaption` |
| Lý do tạo website | `reason` (mỗi chuỗi là một đoạn), `signature` |
| Timeline | Mảng `timeline`: ngày, tiêu đề, mô tả, biểu tượng, ảnh, alt, nhãn |
| Bản đồ | `mapImage` và mảng `places` |
| Album | Mảng `photos`: `image`, `alt`, `caption` |
| Những điều yêu | Mảng `love`: `title`, `text` |
| Quiz | Mảng `quiz`: `question`, `options`, `correct`, `yes`, `no` |
| Thư ngắn | Mảng `letters`: giữ `id` duy nhất, thay `title`, `text`, `quote` |
| Thư cuối | `finalLetter.title`, `paragraphs`, `signature` |
| Quà | `gift.title`, `text`, `image`, `alt`, `invitation` |
| Nhạc | `audioSrc` |
| Bỏ thời gian chờ để thử | `bypassCountdown: true` |

Tên được viết trong nội dung thư và chữ ký cũng cần thay thủ công cho đúng người gửi.

### Ngày tháng

Hai bộ đếm dùng ISO 8601 có múi giờ rõ ràng:

```js
startDate: "2024-02-14T00:00:00+07:00",
targetDate: "2027-02-14T19:00:00+07:00",
```

`+07:00` là giờ Việt Nam. Ngày trong timeline/bản đồ dùng `YYYY-MM-DD`. Số ngày bên nhau là số chu kỳ 24 giờ đầy đủ kể từ thời điểm bắt đầu, kèm giờ/phút/giây còn lại. Ngày tương lai hiển thị 0, không âm. Countdown tự cập nhật mỗi giây và khi quay lại tab; ngày đã qua hiển thị toàn số 0. Ngày mục tiêu không hợp lệ sẽ khóa quà và hiện thông báo cấu hình.

### Thêm ảnh

1. Đặt ảnh trong `assets/images/`, ví dụ `di-bien.webp`.
2. Sửa đường dẫn thành `assets/images/di-bien.webp` và mô tả `alt` phù hợp.
3. Dùng tên tệp không dấu, không khoảng trắng và đúng chữ hoa/thường: GitHub Pages phân biệt hoa/thường.

Ảnh WebP/JPEG rộng khoảng 1200–1600px, thường dưới 300KB là hợp lý. Hero hợp ảnh dọc; timeline hợp ảnh ngang. Ảnh dùng `object-fit` nên có thể cắt một phần khung hình nhưng không bị kéo méo; lightbox dùng `contain` để xem trọn ảnh. Ảnh phía dưới tải khi gần vùng xem. Đường dẫn ảnh sai sẽ dùng `photo-placeholder.svg` thay thế. Giữ tệp dự phòng này trong repository.

### Bản đồ và timeline

Sao chép một đối tượng có sẵn trong `timeline` hoặc `places` để thêm mục, hoặc xóa cả đối tượng để bỏ mục. Giữ timeline theo thứ tự thời gian bạn muốn kể.

`places.x` và `places.y` là phần trăm tính từ góc trên trái ảnh bản đồ, nên đặt từ 8 đến 92 và giãn ghim để dễ bấm. Khi thay ảnh nền, điều chỉnh lại tọa độ. Bản đồ chỉ là minh họa, không biểu diễn khoảng cách địa lý chính xác. Danh sách tên địa điểm bên dưới cũng mở được cùng nội dung, hữu ích trên màn hình nhỏ.

### Quiz và trạng thái

Mỗi câu nên có 3–4 lựa chọn. `correct: 0` chỉ đáp án đầu tiên, `1` là đáp án thứ hai. Thay `yes` và `no` tương ứng; đáp sai vẫn được đi tiếp. Hoàn thành tất cả câu sẽ nhận chìa khóa, không yêu cầu điểm tối thiểu. Chơi lại không thu hồi chìa khóa đã có.

Chỉ lưu `quizComplete` và danh sách ID thư đã mở trong `localStorage`, không lưu câu trả lời hay dữ liệu nhạy cảm. Nếu storage bị chặn/hỏng, trang vẫn hoạt động bằng bộ nhớ phiên hiện tại; tiến độ có thể mất khi tải lại. Muốn bắt đầu một món quà mới, đổi `storageKey` từ `our-little-universe-v1` sang `our-little-universe-v2`.

### Nhạc

Đặt tệp MP3/OGG hợp lệ mà bạn có quyền sử dụng trong `assets/audio/`, rồi sửa:

```js
audioSrc: "assets/audio/our-song.mp3",
```

Nhạc chỉ phát khi bấm **Bật nhạc**, có thể tắt bất cứ lúc nào. Nút bắt đầu hành trình chuyển xuống nội dung. Không tự phát âm thanh. Khi `audioSrc` trống, nút hiển thị **Chưa có nhạc** và bị vô hiệu hóa. Nếu file thiếu/sai định dạng, nút báo nhạc chưa khả dụng; phần còn lại vẫn dùng được. Trình duyệt có thể ghi lỗi mạng cho tài nguyên do bạn cấu hình sai.

### Quà và cách thử mở khóa

Phiên bản mẫu dùng **lời mời đi chơi và ảnh cục bộ**, không nhúng video/playlist nên không cần dịch vụ ngoài hay xử lý embed bị chặn. Lời mời vẫn đọc được nếu ảnh quà lỗi nhờ ảnh dự phòng. Thay `gift` bằng lời mời của riêng bạn.

Để thử: đổi `bypassCountdown: true`, tải lại, làm xong quiz rồi bấm **Mở món quà**. Trước khi gửi tặng, đặt lại `false` và kiểm tra `targetDate`. Cờ thử nghiệm chỉ bỏ thời gian chờ, vẫn yêu cầu quiz. Không có mật khẩu frontend.

**Đây là hiệu ứng khám phá, không phải bảo mật.** Người xem có thể đọc mã nguồn, sửa giờ máy, JavaScript và localStorage. Không đặt mật khẩu, địa chỉ nhà, dữ liệu nhạy cảm hay món quà thực sự bí mật trong repository public. Chỉ dùng ảnh có sự đồng ý của người xuất hiện; xóa metadata vị trí nếu cần. Nếu từng đưa dữ liệu riêng tư vào Git, xóa ở bản mới không tự xóa lịch sử commit.

## Deploy lên GitHub Pages

1. Tạo repository trên GitHub. Với tài khoản miễn phí, có thể dùng repository public cho Pages; chỉ đưa nội dung bạn đồng ý công khai.
2. Đưa các tệp/thư mục ở đây lên thư mục gốc của nhánh bạn chọn, ví dụ `main`. Đảm bảo có `index.html`, `.nojekyll`, `css/`, `js/`, `assets/`.
3. Vào **Settings → Pages → Build and deployment → Source → Deploy from a branch**.
4. Chọn nhánh chứa mã nguồn và thư mục **/(root)**, rồi **Save**.
5. Chờ triển khai xong, mở URL do GitHub Pages cung cấp. Kiểm tra trên điện thoại trước khi chia sẻ.

Không cần thêm bước npm/build hoặc đổi tên repository trong mã. Toàn bộ asset dùng đường dẫn tương đối để chạy dưới `https://<user>.github.io/<repository>/`.

Tham khảo: [GitHub — Configuring a publishing source](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site).

## Kiểm tra và khả năng truy cập

Đã kiểm tra trên Edge Chromium headless: 320, 375, 768, 1024, 1440px không tràn ngang; mở qua đường dẫn con và trực tiếp `file://`; tài nguyên cục bộ; timeline; cả bốn ghim; lightbox mũi tên/trước/sau; Escape/nhấn nền đóng dialog; Tab giữ focus và trả focus về nút nguồn; quiz đúng/sai/chơi lại/lưu trạng thái; thư ngắn lưu trạng thái; thư cuối; countdown tương lai/đã qua/không hợp lệ; quà với cả hai điều kiện; storage hỏng/bị chặn; giảm chuyển động và dọn confetti. Bộ kiểm tra ghi kết quả và ảnh chụp vào `tests/artifacts/` (được Git bỏ qua).

Chạy lại bộ kiểm tra tùy chọn trên máy Windows có Edge và Python:

```sh
python -m pip install playwright
python tests/browser_check.py
```

Playwright chỉ phục vụ kiểm thử, không được tải vào website. Với hệ điều hành khác, có thể đổi `channel='msedge'` trong script sang trình duyệt đã cài phù hợp. JavaScript có thể kiểm tra cú pháp bằng `node --check js/app.js` và tương tự cho bốn tệp còn lại; Node không cần để chạy website.

Giao diện có semantic headings, nút thật, nhãn cho các điều khiển, alt ảnh, focus rõ, skip link, dialog native, vùng bấm ít nhất 44px cho điều khiển chính và `prefers-reduced-motion`. Font hệ thống có fallback, không dùng font bên ngoài. Đồng hồ không đọc lại mỗi giây qua screen reader.

Chưa kiểm chứng trên thiết bị iOS/Android thật hoặc screen reader; nên thử thêm Safari/iPhone và VoiceOver/TalkBack trước khi gửi. Chưa xuất bản lên GitHub hoặc thử nhạc cá nhân vì chưa có repository đích và tệp nhạc thật.

## Những gì cần chuẩn bị trước khi tặng

- Tên/biệt danh, ngày bắt đầu và ngày hẹn thật.
- Ảnh hero, ảnh timeline/album/địa điểm, cùng lời chú thích và alt.
- Câu chuyện, lý do, những điều yêu, 5 câu hỏi và đáp án.
- Bốn thư ngắn, thư cuối, chữ ký và nội dung lời mời/quà.
- Nhạc có quyền sử dụng (tùy chọn).
- Kiểm tra `bypassCountdown: false`, và xem lại toàn bộ nội dung công khai.
