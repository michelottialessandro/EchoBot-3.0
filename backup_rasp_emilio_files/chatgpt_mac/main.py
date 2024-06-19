import random
import argparse
import os
import wave
import pvporcupine
from pvrecorder import PvRecorder
import speech_recognition as sr
import websocket
from scipy.io import wavfile
import json
import serial
arduino = serial.Serial(port='/dev/ttyUSB0', baudrate=115200, timeout=1) #LASCIA TIMEOUT A !

r = sr.Recognizer() # Crea una istanza del recognizer

ACCESS_KEY="zvo3gDplLoZ2lxzG31HCdEdqoNemPth79NuTZqA5LpU6DteiwTlNXg=="
KEYWORD_PATH="Hey-computer_en_raspberry-pi_v3_0_0.ppn"



phrases=["i am listening, please go on","i am listening","i am all ears","Go ahead, I'm listening intently","I'm here to listen"]
        



def send_wav_file_and_get_response(websocket_url,data):
    print("sending")
    ws=websocket.create_connection(websocket_url)
    ws.send(data,websocket.ABNF.OPCODE_BINARY)
    response= ws.recv()
    ws.close()
    return response

# WebSocket URL
websocket_url = "ws://192.168.178.185:8765"


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '--access_key',
        help='AccessKey obtained from Picovoice Console (https://console.picovoice.ai/)')

    parser.add_argument(
        '--keywords',
        nargs='+',
        help='List of default keywords for detection. Available keywords: %s' % ', '.join(
            '%s' % w for w in sorted(pvporcupine.KEYWORDS)),
        choices=sorted(pvporcupine.KEYWORDS),
        metavar='')

    parser.add_argument(
        '--keyword_paths',
        nargs='+',
        help="Absolute paths to keyword model files. If not set it will be populated from `--keywords` argument")

    parser.add_argument(
        '--library_path',
        help='Absolute path to dynamic library. Default: using the library provided by `pvporcupine`')

    parser.add_argument(
        '--model_path',
        help='Absolute path to the file containing model parameters. '
             'Default: using the library provided by `pvporcupine`')

    parser.add_argument(
        '--sensitivities',
        nargs='+',
        help="Sensitivities for detecting keywords. Each value should be a number within [0, 1]. A higher "
             "sensitivity results in fewer misses at the cost of increasing the false alarm rate. If not set 0.5 "
             "will be used.",
        type=float,
        default=None)

    parser.add_argument('--audio_device_index', help='Index of input audio device.', type=int, default=-1)

    parser.add_argument('--output_path', help='Absolute path to recorded audio for debugging.', default=None)

    parser.add_argument('--show_audio_devices', action='store_true')

    args = parser.parse_args()

    if args.show_audio_devices:
        for i, device in enumerate(PvRecorder.get_available_devices()):
            print('Device %d: %s' % (i, device))
        return

    if args.keyword_paths is None:
        if args.keywords is None:
            raise ValueError("Either `--keywords` or `--keyword_paths` must be set.")

        keyword_paths = [pvporcupine.KEYWORD_PATHS[x] for x in args.keywords]
    else:
        keyword_paths = args.keyword_paths

    if args.sensitivities is None:
        args.sensitivities = [0.5] * len(keyword_paths)

    if len(keyword_paths) != len(args.sensitivities):
        raise ValueError('Number of keywords does not match the number of sensitivities.')

    try:
        porcupine = pvporcupine.create(
            access_key=ACCESS_KEY,
            library_path=args.library_path,
            model_path=args.model_path,
            keyword_paths=args.keyword_paths,
            sensitivities=args.sensitivities)
    except pvporcupine.PorcupineInvalidArgumentError as e:
        print("One or more arguments provided to Porcupine is invalid: ", args)
        print(e)
        raise e
    except pvporcupine.PorcupineActivationError as e:
        print("AccessKey activation error")
        raise e
    except pvporcupine.PorcupineActivationLimitError as e:
        print("AccessKey '%s' has reached it's temporary device limit" % args.access_key)
        raise e
    except pvporcupine.PorcupineActivationRefusedError as e:
        print("AccessKey '%s' refused" % args.access_key)
        raise e
    except pvporcupine.PorcupineActivationThrottledError as e:
        print("AccessKey '%s' has been throttled" % args.access_key)
        raise e
    except pvporcupine.PorcupineError as e:
        print("Failed to initialize Porcupine")
        raise e

    keywords = list()
    for x in keyword_paths:
        keyword_phrase_part = os.path.basename(x).replace('.ppn', '').split('_')
        if len(keyword_phrase_part) > 6:
            keywords.append(' '.join(keyword_phrase_part[0:-6]))
        else:
            keywords.append(keyword_phrase_part[0])

    print('Porcupine version: %s' % porcupine.version)

    recorder = PvRecorder(
        frame_length=porcupine.frame_length,
        device_index=args.audio_device_index)
    recorder.start()

    wav_file = None
    if args.output_path is not None:
        wav_file = wave.open(args.output_path, "w")
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(16000)
        

    print('Listening ... (press Ctrl+C to exit)')    
    try:
        while True:
            pcm = recorder.read()
            result = porcupine.process(pcm)

            if result >= 0:
                #print('[%s] Detected %s' % (str(datetime.now()), keywords[result]))
                print("im listening please go on")
                phrase = phrases[random.randint(0,len(phrases)-1)]
                command=f'echo "{phrase}" |   ./piper/piper --model piper/en_US-kathleen-low.onnx --config piper/en_en_US_kathleen_low_en_US-kathleen-low.onnx.json --output-raw |   aplay -r 16000 -f S16_LE -t raw -'
                os.system(command)
                arduino.write(bytes("listening"+'\n','utf-8'))

                with sr.Microphone() as source:
                    print("Say something!")
                    audio = r.listen(source,)
                arduino.write(bytes("led_stop"+'\n','utf-8'))
                result=send_wav_file_and_get_response(websocket_url=websocket_url,data=audio.get_wav_data())
                result=json.loads(result)
                print(result)
                if(result["lan"]=="it"):
                    command=f'echo "{result["text"]}" |   ./piper/piper --model piper/it_IT-riccardo-x_low.onnx --config piper/it_it_IT_riccardo_x_low_it_IT-riccardo-x_low.onnx.json --output-raw |   aplay -r 16000 -f S16_LE -t raw -'
                else:
                    command=f'echo "{result["text"]}" |   ./piper/piper --model piper/en_US-kathleen-low.onnx --config piper/en_en_US_kathleen_low_en_US-kathleen-low.onnx.json --output-raw |   aplay -r 16000 -f S16_LE -t raw -'
                os.system(command)
    except KeyboardInterrupt:
        print('Stopping ...')
    finally:
        recorder.delete()
        porcupine.delete()
        


if __name__ == '__main__':
    main()
