import os
import gc
import asyncio
import subprocess
import requests
import edge_tts
from mutagen.mp3 import MP3

# आज की तारीख का फोल्डर
BASE_DIR = "2026-11-13_Project_18_9Hz"
os.makedirs(f"{BASE_DIR}/audio", exist_ok=True)
os.makedirs(f"{BASE_DIR}/stock", exist_ok=True)
os.makedirs(f"{BASE_DIR}/parts", exist_ok=True)

PEXELS_API_KEY = os.environ.get("PEXELS_API_KEY", "").strip()
MIN_PART_SECONDS = 192.0  # 8 x 192s = 1536s (25 मिनट 36 सेकंड गारंटीड)

STORY_PARTS = {
    1: {
        "narration": """क्या आपने कभी सोचा है कि जब किसी खाली कमरे में अचानक आपकी रीढ़ की हड्डी में ठंडक दौड़ती है, तो वो डर होता है... या फिज़िक्स? मेरा नाम आरव है, और तीन दिन पहले तक मेरे लिए भूत सिर्फ़ कमज़ोर दिमाग का एक केमिकल लोचा था। लेकिन फिर मैंने 5 लाख की वो शर्त लगा ली। रात के ठीक 12 बजे, जब मुंबई की उस 120 साल पुरानी बंद पड़ी कॉटन मिल के लोहे के गेट पर बाहर से ताला जड़ा गया, तो मेरे हाथ में कोई ताबीज़ नहीं था... मेरे पास था एक थर्मल कैमरा, एक EMF मीटर, और 18 हर्ट्ज़ पकड़ने वाला माइक। पहले दस मिनट बिल्कुल सन्नाटा रहा। लेकिन 12 बजकर 14 मिनट पर... मुझे अचानक ताज़ा भुनी हुई कॉफी की खुशबू आई। एक ऐसी जगह पर, जहाँ 40 साल से बिजली का एक तार भी नहीं जुड़ा था। मैंने हँसकर कैमरा घुमाया—और तभी स्क्रीन पर वो दिखा, जिसने मेरा गला सुखा दिया। पूरे कमरे का तापमान 28 डिग्री था, सिवाय एक कोने के... जहाँ तापमान 4 डिग्री सेल्सियस दिखा रहा था, बिल्कुल एक इंसान के आकार में। मैंने तुरंत अपना साउंड एनालाइज़र ऑन किया। स्क्रीन पर 18.9 हर्ट्ज़ की एक सीधी लाल लाइन चमक रही थी। साइंस कहता है कि 18.9 हर्ट्ज़ की इन्फ्रासाउंड तरंगें इंसान की आँखों के पर्दे में कंपन पैदा करती हैं, जिससे दिमाग को सामने भूत दिखने का भ्रम होता है। मैं राहत से मुस्कुराया—चलो, विज्ञान जीत गया। लेकिन तभी... मेरी पीठ के ठीक दो इंच पीछे से किसी ने मेरे कान में धीमे से फुसफुसाया। मैंने काँपते हाथों से अपने साउंड मीटर की तरफ़ देखा... और उस वक्त मेरा 18.9 हर्ट्ज़ डिटेक्टर बिल्कुल शांत था।""",
        "queries": ["abandoned factory night", "flashlight dark corridor", "infrared thermal camera", "audio waveform screen", "scared man dark"]
    },
    2: {
        "narration": """आरव बिजली की रफ़्तार से पीछे पलटा, लेकिन टॉर्च की रोशनी में सिर्फ़ धूल के उड़ते कण थे... वहाँ कोई नहीं था। तभी उसकी नज़र छत के जंग लगे लोहे के पाइपों पर पड़ी, जहाँ से तेज़ हवा टकराकर सीटी जैसी आवाज़ बना रही थी। आरव ने अपना जैकेट उतारकर उस टूटे पाइप के मुँह पर कसकर बाँध दिया। लेकिन 30 सेकंड भी नहीं बीते थे कि मीटर की सुई फिर से लाल निशान पर पहुँच गई। आरव ने माइक को ज़मीन से सटाया। स्पेक्ट्रम एनालाइज़र ने जो दिखाया वह नामुमकिन था—यह आवाज़ छत से नहीं, बल्कि उसके पैरों के 10 फीट नीचे ज़मीन के अंदर से आ रही थी। तभी उसके जूते के नीचे 1982 का एक आधा जला हुआ मिल का रजिस्टर मिला। उस रजिस्टर के आखिरी पन्ने पर ठीक आज ही की तारीख—13 नवंबर—दर्ज थी। और जब उसने लाइव स्ट्रीम कर रहे अपने फोन की तरफ देखा, तो बंद स्क्रीन पर अंदर की तरफ़ से धुंधली उंगलियों के निशान धीरे-धीरे उभरने लगे।""",
        "queries": ["rusty industrial pipes dark", "concrete floor dust flashlight", "old burnt book paper", "dark smartphone screen", "creepy shadow hallway"]
    },
    3: {
        "narration": """आरव ने अपनी टॉर्च मिल की पुरानी लाल ईंटों वाली दीवार पर मारी—ईंटों में छोटे-छोटे चमकते हुए कण दिख रहे थे। अचानक उसके दिमाग में 'स्टोन टेप थ्योरी' कौंधी। विज्ञान में एक थ्योरी है कि जिन दीवारों में आयरन ऑक्साइड और क्वार्ट्ज़ क्रिस्टल ज़्यादा होते हैं, वे किसी पुराने कैसेट टेप की तरह तेज़ इलेक्ट्रोमैग्नेटिक ऊर्जा को रिकॉर्ड कर सकती हैं। आरव ने दीवार की ईंटों पर हल्का करंट छोड़ा और अपना स्पीकर ऑन किया। 20 सेकंड बाद स्पीकर से 1982 की मशीनों का शोर और दर्जनों लोगों की चीखें साफ़ सुनाई देने लगीं। आरव खुश हो गया—उसने भूत को साइंस से डीकोड कर लिया था! लेकिन तभी मशीनों का शोर अचानक कट गया... और उस 40 साल पुरानी रिकॉर्डिंग के बीच से एक भारी आवाज़ ने साफ़ हिंदी में कहा—'आरव... बाहर मत जाओ।'""",
        "queries": ["old red brick wall texture", "electronic circuit wires battery", "vintage audio speaker dark", "shocked face dark lighting", "dark empty warehouse"]
    },
    4: {
        "narration": """अचानक आरव का सिर तेज़ी से घूमने लगा और सामने की दीवार से एक लंबा काला साया बाहर निकलता दिखा। तभी उसकी बेल्ट पर लगा कार्बन मोनोऑक्साइड डिटेक्टर ज़ोर-ज़ोर से बीप करने लगा! कमरे में ज़हरीली गैस लीक हो रही थी। आरव ने एक भारी लोहे की रॉड उठाई और पुरानी काँच की खिड़की तोड़ दी। ताज़ा हवा अंदर आते ही उसका सिर हल्का हुआ और वह साया गायब हो गया। आरव हँस पड़ा—हर भूत के पीछे कोई न कोई गैस होती है। लेकिन जब उसने कोने में लगे बैकअप कैमरे की फुटेज रिवाइंड करके देखी, तो उसके चेहरे से हँसी गायब हो गई। वीडियो में उस काले साये ने सचमुच कमरे के बीच रखी एक भारी लोहे की कुर्सी को घसीटकर दरवाज़े के सामने लगा दिया था। ज़हरीली गैस लोहे की कुर्सी नहीं हिला सकती।""",
        "queries": ["smoke fog dark room", "digital alarm sensor red light", "broken glass window night", "empty chair dark room", "man watching laptop dark"]
    },
    5: {
        "narration": """अब आरव के पास कोई बहाना नहीं बचा था। वह दरवाज़े से कुर्सी हटाकर बेसमेंट की टूटी सीढ़ियों से नीचे उतरा। कोने में एक 1980 के दशक का विशाल डीज़ल जनरेटर रखा था, जिसके सारे तार कटे हुए थे। लेकिन थर्मल कैमरे में वह जनरेटर बिना किसी ईंधन के 90 डिग्री पर लाल दहक रहा था। आरव का EMF मीटर 100 मिलीगॉस के पार चला गया। वह ऊर्जा का पीछा करते हुए एक भारी स्टील के दरवाज़े तक पहुँचा, जिस पर लिखा था—'लैब 4'। अंदर तांबे के विशाल कॉइल्स और पुराने ऑसिलोस्कोप लगे थे। मेज़ पर धूल के बीच एक पुरानी रंगीन तस्वीर पड़ी थी—वह आरव के खुद के बचपन की तस्वीर थी, जो कल रात तक उसके घर की अलमारी में रखी थी।""",
        "queries": ["dark underground stairs", "old diesel generator industrial", "oscilloscope green wave screen", "rusted metal door basement", "vintage photograph dusty table"]
    },
    6: {
        "narration": """आरव ने तस्वीर के नीचे दबी चमड़े की पुरानी डायरी निकाली। पहले पन्ने पर नाम लिखा था—'डॉ. विश्वनाथ शर्मा, चीफ साइंटिस्ट, 1982'। वह आरव के खुद के दादाजी थे! डायरी में लिखा था कि यह मिल एक गुप्त बायो-इलेक्ट्रोमैग्नेटिक प्रोजेक्ट का अड्डा थी, जहाँ वैज्ञानिक साबित कर रहे थे कि मौत के बाद इंसान की चेतना मैग्नेटिक फील्ड में कैद की जा सकती है। आखिरी पन्ने पर लिखा था—'13 नवंबर 1982: कंटेनमेंट टूट गया, यह चीज़ बिजली और इंसानी गर्मी से ज़िंदा रहती है।' तभी धड़ाम से लैब 4 का दरवाज़ा लॉक हो गया! तापमान -2 डिग्री पर गिर गया, हवा में नीली चिंगारियाँ चमकीं, और आरव की स्मार्टवॉच की बैटरी 100% से सीधे 1% पर आ गई।""",
        "queries": ["old leather diary book dark", "handwritten science notes vintage", "frost ice mist dark room", "blue electric sparks dark", "smartwatch low battery dark"]
    },
    7: {
        "narration": """वह काला साया तेज़ी से आरव की तरफ़ बढ़ रहा था। भागने का कोई रास्ता नहीं था। लेकिन आरव का इंजीनियर दिमाग दौड़ा—अगर यह एंटिटी इलेक्ट्रोमैग्नेटिक फील्ड से बनी है, तो एक रिवर्स-फेज़ EMP शॉक इसे बिखेर सकता है! उसने तुरंत अपने कैमरे का हाई-वोल्टेज फ्लैश कैपेसिटर तोड़ा, तांबे का तार लपेटा और पावर बैंक से जोड़ दिया। ठीक उसी पल बर्फ़ जैसा ठंडा हाथ उसके गले पर कस गया। आखिरी सेकंड में आरव ने दोनों खुले तार जोड़ दिए! एक तेज़ नीली इलेक्ट्रिक चमक और कान फाड़ देने वाली शॉकवेव पूरे कमरे में फूट पड़ी। काँच के सारे चैंबर चकनाचूर हो गए और वह साया धुएँ में बदलकर गायब हो गया। आरव ज़मीन पर गिर पड़ा... लेकिन तभी 40 साल से बंद इस मिल की सारी ट्यूबलाइट्स एक साथ जल उठीं।""",
        "queries": ["soldering copper wires sparks", "dark shadow silhouette fog", "blue lightning flash explosion", "shattered glass floor dark", "flickering fluorescent light hallway"]
    },
    8: {
        "narration": """लैब का लॉक खुलते ही आरव बाहर भागा। अगले दो दिनों तक उसने अपनी सारी रिकॉर्डिंग—थर्मल फुटेज, 18.9 हर्ट्ज़ की वेव्स और 100 मिलीगॉस का EMF स्पाइक—लैपटॉप पर एनालाइज़ की। हर एक फाइल 100% असली थी। आरव ने विज्ञान और पैरानॉर्मल की दुनिया को हिला देने वाला पहला ठोस सबूत दुनिया के सामने रख दिया। तीन दिन बाद वह पहली बार चैन की नींद सोने के लिए बिस्तर पर लेटा। ठीक 3 बजकर 1 मिनट पर... आरव की नींद एक तेज़ ठंड से खुली। उसके बेडरूम का डिजिटल थर्मोस्टेट लाल चमक रहा था—तापमान 4 डिग्री सेल्सियस। और टेबल पर रखे बंद लैपटॉप की स्क्रीन अपने आप ऑन हुई... माइक पर वही 18.9 हर्ट्ज़ की सीधी लाल लाइन फिर से बननी शुरू हो गई। वह ऊर्जा आरव के बैकअप डेटा के साथ उसके घर आ चुकी थी।""",
        "queries": ["city sunrise morning mist", "laptop data analysis dark room", "dark bedroom night window", "digital clock 3am red", "laptop glowing dark room"]
    }
}

def download_pexels_video(query, out_path):
    if not PEXELS_API_KEY:
        return False
    try:
        headers = {"Authorization": PEXELS_API_KEY}
        url = f"https://api.pexels.com/videos/search?query={query}&per_page=3&orientation=landscape"
        r = requests.get(url, headers=headers, timeout=15).json()
        videos = r.get("videos", [])
        if not videos:
            return False
        for vf in videos[0].get("video_files", []):
            if vf.get("width", 0) >= 1280:
                vid_data = requests.get(vf["link"], timeout=30).content
                with open(out_path, "wb") as f:
                    f.write(vid_data)
                return True
        link = videos[0]["video_files"][0]["link"]
        with open(out_path, "wb") as f:
            f.write(requests.get(link, timeout=30).content)
        return True
    except Exception as e:
        print(f"Pexels fallback for '{query}': {e}")
        return False

async def make_voice(text, out_path):
    comm = edge_tts.Communicate(text=text.strip(), voice="hi-IN-MadhurNeural", rate="-10%", pitch="-4Hz")
    await comm.save(out_path)

async def main():
    part_videos = []
    for part_id, data in STORY_PARTS.items():
        final_part = f"{BASE_DIR}/parts/part_{part_id:02d}.mp4"
        if os.path.exists(final_part):
            part_videos.append(final_part)
            continue

        raw_mp3 = f"{BASE_DIR}/audio/part_{part_id:02d}_raw.mp3"
        if not os.path.exists(raw_mp3):
            await make_voice(data["narration"], raw_mp3)

        voice_dur = MP3(raw_mp3).info.length
        target_dur = max(voice_dur + 4.0, MIN_PART_SECONDS)
        print(f"[Part {part_id}/8] Voice={voice_dur:.1f}s -> Target={target_dur:.1f}s")

        padded_wav = f"/tmp/voice_pad_{part_id}.wav"
        subprocess.run([
            "ffmpeg", "-y", "-i", raw_mp3,
            "-af", f"apad=whole_dur={target_dur:.2f}",
            padded_wav
        ], check=True)

        queries = data["queries"]
        clip_dur = target_dur / len(queries)
        clip_list = f"/tmp/clips_{part_id}.txt"

        with open(clip_list, "w") as f:
            for idx, q in enumerate(queries):
                raw_clip = f"{BASE_DIR}/stock/p{part_id}_q{idx}.mp4"
                graded_clip = f"/tmp/p{part_id}_graded_{idx}.mp4"

                if not os.path.exists(raw_clip):
                    ok = download_pexels_video(q, raw_clip)
                else:
                    ok = True

                if ok and os.path.exists(raw_clip):
                    subprocess.run([
                        "ffmpeg", "-y", "-stream_loop", "-1", "-i", raw_clip,
                        "-t", f"{clip_dur:.2f}", "-an",
                        "-vf", "scale=1280:720:force_original_aspect_ratio=increase,crop=1280:720,eq=brightness=-0.10:contrast=1.25:saturation=0.50,vignette=PI/4,fps=24",
                        "-c:v", "libx264", "-preset", "fast", "-pix_fmt", "yuv420p", graded_clip
                    ], check=True)
                else:
                    subprocess.run([
                        "ffmpeg", "-y", "-f", "lavfi",
                        "-i", f"color=c=#080c14:s=1280x720:d={clip_dur:.2f}:r=24",
                        "-vf", "noise=alls=12:allf=t+u,vignette=PI/3",
                        "-c:v", "libx264", "-pix_fmt", "yuv420p", graded_clip
                    ], check=True)

                f.write(f"file '{graded_clip}'\n")

        raw_vid = f"/tmp/raw_part_{part_id}.mp4"
        subprocess.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", clip_list, "-c", "copy", raw_vid], check=True)

        drone_wav = f"/tmp/drone_{part_id}.wav"
        subprocess.run([
            "ffmpeg", "-y", "-f", "lavfi",
            "-i", f"aevalsrc=0.14*sin(2*PI*55*t)+0.09*sin(2*PI*18.9*t):s=44100:d={target_dur:.2f}",
            drone_wav
        ], check=True)

        subprocess.run([
            "ffmpeg", "-y", "-i", raw_vid, "-i", padded_wav, "-i", drone_wav,
            "-filter_complex", "[1:a]volume=1.0[vo];[2:a]volume=0.25[bg];[vo][bg]amix=inputs=2:duration=first[aout]",
            "-map", "0:v", "-map", "[aout]", "-c:v", "copy", "-c:a", "aac", "-shortest", final_part
        ], check=True)

        part_videos.append(final_part)
        gc.collect()

    with open("/tmp/all_parts.txt", "w") as f:
        for pv in part_videos:
            f.write(f"file '{pv}'\n")

    final_master = f"{BASE_DIR}/FINAL_25MIN_HORROR_2026-11-13.mp4"
    subprocess.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", "/tmp/all_parts.txt", "-c", "copy", final_master], check=True)
    print(f"SUCCESS! 25+ Min Video Ready: {final_master}")

if __name__ == "__main__":
    asyncio.run(main())
