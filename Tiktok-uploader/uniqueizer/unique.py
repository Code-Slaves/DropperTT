from moviepy.editor import VideoFileClip, ImageSequenceClip
from moviepy.audio.AudioClip import AudioClip
from moviepy.audio.AudioClip import AudioArrayClip
from pydub import AudioSegment
import gc
from pydub.utils import mediainfo
import numpy as np
import cupy as cp
import cv2
from concurrent.futures import ThreadPoolExecutor
import multiprocessing
import time




class Unique():
    def __init__(self, video_path_input:str, video_path_output:str):
        start_time = time.time()

        video = VideoFileClip(video_path_input)

        self.original_height = video.size[1]
        self.original_width =  video.size[0]

        # Обработка кадров видео и создание нового видеоклипа
        processed_frames = self.process_video_frames(video, self.process_frame_batch, batch_size=10)  # установите нужный размер пакета
        new_video = ImageSequenceClip(processed_frames, fps=video.fps)

        if video.audio is not None:
            original_audio = video.audio
            audio_segment = AudioSegment(
                # Конвертация данных аудио в формат, с которым может работать pydub
                data=np.array(original_audio.to_soundarray() * 32768, dtype=np.int16).tobytes(),
                sample_width=2,  # pydub работает с 2 байтами = 16 бит
                frame_rate=original_audio.fps,
                channels=original_audio.nchannels
            )

            # Применение искажения к аудио
            processed_audio = self.distort_audio(audio_segment)

            # Конвертация обработанного аудио обратно в формат, совместимый с moviepy
            processed_audio_data = np.frombuffer(processed_audio.raw_data, np.int16).reshape((-1, processed_audio.channels))
            processed_audio_data = processed_audio_data.astype(np.float32) / 32768  # moviepy ожидает float32

            # Создание аудиоклипа для moviepy
            new_audio_clip = AudioArrayClip(processed_audio_data, fps=processed_audio.frame_rate)

            # Добавление аудио к видеоклипу
            new_video = new_video.set_audio(new_audio_clip)

        # Экспорт готового видео
        new_video.write_videofile(video_path_output, codec='libx264', audio_codec='aac')
        self.release_ram()

        with open(f"{video_path_output}", "rb") as vid:
            self.baytes =  vid.read()


        end_time = time.time()
        print(f"Время выполнения: {end_time - start_time} секунд")

        


    def worker_init(self):
        global cv2

    def process_frame_batch(self, frame_batch):
        processed_frames = []

        for image_frame in frame_batch:
            # Создаем копию кадра, чтобы не изменять оригинал
            modifiable_frame = cp.array(image_frame)  # Теперь мы используем CuPy

            # Преобразуем обычное изображение в GPU изображение
            gpu_frame = cv2.cuda_GpuMat()
            gpu_frame.upload(modifiable_frame.get())# Получаем np.array из CuPy array для загрузки в GpuMat

            gpu_frame = cv2.cuda.resize(gpu_frame, (self.original_width, self.original_height))


            # Создание шума типа "соль и перец" с использованием CuPy и применение его к изображению на GPU
            noise = cp.random.randint(10, 35, modifiable_frame.shape, dtype=cp.uint8)

            # Вместо этого, преобразуйте CuPy array в NumPy array перед загрузкой в GpuMat
            noise_np = cp.asnumpy(noise)  # Преобразование в NumPy array
            noise_gpu = cv2.cuda_GpuMat()  # Создаем пустой GpuMat
            noise_gpu.upload(noise_np)  # Загружаем NumPy array в GpuMa  

            noisy_frame_gpu = cv2.cuda.add(gpu_frame, noise_gpu)

            gpu_frame.release()
            noise_gpu.release()
            del gpu_frame, noise, noise_np, noise_gpu

            # Рандомизация гауссова размытия
            kernel_size = int(cp.random.randint(1, 2) * 2 + 1)  # дает нечетное число от 3 до 13
            sigmaX = float(cp.random.uniform(0.1, 0.3))

            # Создаем объект размытия на GPU и применяем его
            blur_filter = cv2.cuda.createGaussianFilter(noisy_frame_gpu.type(), -1, (kernel_size, kernel_size), sigmaX)
            blurred_frame = blur_filter.apply(noisy_frame_gpu)

            # Добавляем очень маленькое количество шума (на GPU)
            noise_intensity = float(cp.random.randint(10, 30) / 100.0)
            subtle_noise = cp.random.normal(0, noise_intensity, modifiable_frame.shape).astype(cp.uint8)

            # Convert the CuPy array 'subtle_noise' into a NumPy array and then upload it to a GpuMat object
            subtle_noise_np = cp.asnumpy(subtle_noise)  # Converting to NumPy array
            subtle_noise_gpu = cv2.cuda_GpuMat()  # Creating an empty GpuMat
            subtle_noise_gpu.upload(subtle_noise_np)  # Uploading the NumPy array to GpuMat

            # Now, you can add 'subtle_noise' to 'blurred_frame', as both are GpuMat objects
            noisy_frame_gpu = cv2.cuda.add(blurred_frame, subtle_noise_gpu)

            subtle_noise_gpu.release()
            del kernel_size, sigmaX, blur_filter, noise_intensity, subtle_noise, subtle_noise_np, subtle_noise_gpu

            # Подготовка коэффициентов контраста и яркости
            alpha = float(cp.random.randint(100, 102) / 100.0)  # коэффициент контраста
            beta = float(cp.random.randint(99, 102) / 100.0)    # коэффициент яркости

            # Конвертируем GpuMat обратно в CuPy array и вносим изменения в контраст и яркость
            result_frame_gpu = noisy_frame_gpu.download()
            result_frame = cp.array(result_frame_gpu) * alpha + beta
            result_frame = result_frame.clip(0, 255).astype(cp.uint8)

            # Добавляем обработанный кадр в список
            processed_frames.append(result_frame.get())  # Конвертация обратно в np.array для дальнейшего использования

            del alpha, beta, result_frame_gpu, result_frame
            cp.get_default_memory_pool().free_all_blocks()

        return processed_frames


    def process_video_frames(self, video, effect_function, batch_size=10, workers=6):
        with ThreadPoolExecutor(max_workers=workers) as executor:
            # Создание пакетов кадров для обработки
            frame_batches = list(video.iter_frames(dtype="uint8", fps=video.fps))
            frame_batches = [frame_batches[i:i + batch_size] for i in range(0, len(frame_batches), batch_size)]

            # Отправка пакетов на обработку
            future_to_batch = {executor.submit(effect_function, batch): batch for batch in frame_batches}

            # Сбор обработанных кадров
            processed_frames = []
            for future in future_to_batch:
                processed_frames.extend(future.result())

        return processed_frames


    def distort_audio(self, audio_segment):
        """
        Создает искажение для аудио, просто добавляя шум.

        :param audio_segment: сегмент аудио, который нужно обработать.
        :return: обработанный сегмент аудио.
        """
        # Получение массива аудиоданных
        samples = np.array(audio_segment.get_array_of_samples())

        # Создание шума
        distortion = np.random.uniform(low=-200, high=200, size=len(samples)).astype(np.int16)

        # Добавление шума к аудио
        distorted_samples = samples + distortion

        # Предотвращение переполнения
        np.clip(distorted_samples, -32768, 32767, out=distorted_samples)

        # Создание нового аудио сегмента с измененными сэмплами
        new_audio_segment = audio_segment._spawn(distorted_samples.tobytes())

        return new_audio_segment


    def release_ram(self):
        cp.cuda.Stream.null.synchronize()
        cp.get_default_memory_pool().free_all_blocks()
        gc.collect()





