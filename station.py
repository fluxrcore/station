import argparse
import subprocess
import os

try:
    volume = os.path.join(os.getcwd(), 'data')
except Exception as e:
    print(f"Error occurred while creating volume path: {e}")

def main():
    parser = argparse.ArgumentParser(description="Script to run shell commands based on backend selection")
    parser.add_argument("backend", choices=["huggingface/tgi", "huggingface/tgi-q"], help="Select backend")
    parser.add_argument("device",choices=["gpu","cpu"],help="Set the device (default gpu)",default="gpu")
    parser.add_argument("--model", help="Set the model.")
    #parser.add_argument("--arg2", help="Argument 2")
    parser.add_argument("--quantize", help="Quantization method", default="ct2")
    args = parser.parse_args()

    if args.model is None:
        parser.error("--model is required for all station backends.")

    backend = args.backend.strip()

    backend = backend.lower()

    device = args.device.strip()
    device = device.lower()

    if backend == "huggingface/tgi":
        #model_arg = f"--model-id {args.model}" if args.model else ""
        if device == "cpu":
            command = f"docker run --shm-size 1g -p 8080:80 -v {volume} ghcr.io/huggingface/text-generation-inference:1.4 --model-id {args.model}"
        else:
            command = f"docker run --gpus all --shm-size 1g -p 8080:80 -v {volume} ghcr.io/huggingface/text-generation-inference:1.4 --model-id {args.model}"

    elif backend == "huggingface/tgi-q":
        #model_arg = f"--model-id {args.model}" if args.model else ""
        if device == "cpu":
            command = f"docker run --shm-size 1g -p 8080:80 -v {volume} docker.io/michaelf34/tgi:05-11-2023 --model-id {args.model} --quantize {args.quantize}"
        else:
            command = f"docker run --gpus all --shm-size 1g -p 8080:80 -v {volume} docker.io/michaelf34/tgi:05-11-2023 --model-id {args.model} --quantize {args.quantize}"
    else:
        print("Invalid backend specified")
        return

    try:
        subprocess.run(command, shell=True, check=True)
        #os.system(command)
        print(command)
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        return

if __name__ == "__main__":
    main()
