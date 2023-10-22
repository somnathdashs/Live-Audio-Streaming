from flask import Flask,Response,render_template
import pyaudio

app=Flask(__name__,template_folder="template")

FORMAT=pyaudio.paInt16
CHANNELS=2
RATE=44100
CHUNK=1024
RECORD_SECONDS=5


audio_stream=pyaudio.PyAudio()


def genHeader(sampleRate, bitsPerSample, channels):
    datasize = 2000*10**6
    o = bytes("RIFF",'ascii')                                               # (4byte) Marks file as RIFF
    o += (datasize + 36).to_bytes(4,'little')                               # (4byte) File size in bytes excluding this and RIFF marker
    o += bytes("WAVE",'ascii')                                              # (4byte) File type
    o += bytes("fmt ",'ascii')                                              # (4byte) Format Chunk Marker
    o += (16).to_bytes(4,'little')                                          # (4byte) Length of above format data
    o += (1).to_bytes(2,'little')                                           # (2byte) Format type (1 - PCM)
    o += (channels).to_bytes(2,'little')                                    # (2byte)
    o += (sampleRate).to_bytes(4,'little')                                  # (4byte)
    o += (sampleRate * channels * bitsPerSample // 8).to_bytes(4,'little')  # (4byte)
    o += (channels * bitsPerSample // 8).to_bytes(2,'little')               # (2byte)
    o += (bitsPerSample).to_bytes(2,'little')                               # (2byte)
    o += bytes("data",'ascii')                                              # (4byte) Data Chunk Marker
    o += (datasize).to_bytes(4,'little')                                    # (4byte) Data size in bytes
    return o


def Sound():
    bitspersample=16
    wav_hader=genHeader(RATE,bitspersample,2)
    stream=audio_stream.open(format=FORMAT,channels=2,rate=RATE,input=True,input_device_index=1,frames_per_buffer=CHUNK)
    first_run=True
    while True:
        if first_run:
            data=wav_hader+stream.read(CHUNK)
            first_run=False
        else:
            data=stream.read(CHUNK)
        yield(data)

@app.route('/')
def index():
    return render_template("Audio.html")

@app.route("/audio")
def audio():
    return Response(Sound())

app.run(host="127.0.0.1",port=5454,threaded=True)