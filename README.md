# Blunt

Blunt is an auxiliary tool for subtitle files. It combines subtitles exported from platforms like [Whisper](https://github.com/openai/whisper) or [Azure AI](https://speech.microsoft.com/portal/captioning) with the original manuscript for comparison, ultimately generating a more accurate subtitle file that matches the content better.

Suppose you're creating video content. You might start with an original text that you convert into speech using Text-to-Speech (TTS) software. Then, you merge this audio into a video. Later, you decide to add subtitles and use software that automatically generates subtitles based on the video. You use this software to create subtitles for your video. Everything goes well until you notice some discrepancies between the generated subtitles and your original text. That's when you can use Blunt to help correct these errors in the subtitles, making the subtitle content identical to your original text.

For example, your original text is like this:

```
안녕하세요! 여기서 책을 찾고 계세요?
네, 맞아요. 이 책을 찾고 있어요.
어떤 책을 찾고 계신가요? 제가 도와드릴게요.
이번에 새로 나온 소설 책이에요. 제목은 '사랑의 시'에요.
'사랑의 시'요? 그 책은 저희가 이번 주에 입고를 안 했어요. 죄송해요.
아, 그렇군요. 다음에 다시 오겠습니다. 감사합니다!
네, 언제든지 도와드릴게요. 좋은 하루 되세요!
```

And the subtitles generated by the software appear like this:

```
1
00:00:00,000 --> 00:00:04,980
안녕하세요. 여기서 책을 찾고 계세요?

2
00:00:04,980 --> 00:00:13,120
네, 맞아요. 이 책을 찾고 있어요. 어떤 책을 찾고 계신가요?

3
00:00:13,120 --> 00:00:22,080
제가 도와드릴게요. 이번에 새로 나온 소설 책이에요. 제목은 사랑의 시예요.

4
00:00:22,080 --> 00:00:28,120
사랑의 시요? 그 책은 저희가 이번 주에 입구를 안 했어요.

5
00:00:28,120 --> 00:00:37,440
죄송해요. 아, 그렇군요. 다음에 다시 오겠습니다. 감사합니다.

6
00:00:37,440 --> 00:00:44,240
네, 언제든지 도와드릴게요. 좋은 하루 되세요.

```

You can see there are some differences. Using Blunt would correct these variances. The result is this:

![Comparison](https://raw.githubusercontent.com/t2og/blunt/main/assets/comparison.png)


## Setup

    pip install git+https://github.com/t2og/blunt.git


## Usage in Command-line
Blunt may be used directly in the Command Line Interface (CLI) with a blunt command:

    blunt subtitle.srt original.txt
