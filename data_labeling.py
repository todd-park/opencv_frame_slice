import argparse 
import cv2
import os

def video_name_split_generater(parse_path):
    index_split = parse_path.split('_')
    file_date = index_split[0] + '_' + index_split[1] + '_' + index_split[2]
    start_time = float(index_split[3])
    info_split = index_split[4].split('.')
    ending_point = float(info_split[0])
    return file_date, start_time, ending_point

def is_video_file(filename):
    video_extensions = ['.mp4', '.avi', '.mkv', '.mov', '.flv', '.wmv']
    _, ext = os.path.splitext(filename)
    return ext.lower() in video_extensions


def save_video_frames(video_path, output_dir, filename_format, start_time, ending_range):
    # 동영상 파일을 읽어옴
    video = cv2.VideoCapture(video_path)

    # 동영상의 FPS(프레임)을 구함
    fps = int(video.get(cv2.CAP_PROP_FPS))

    # 출력 디렉토리가 없으면 생성
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 중간 프레임을 계산
    start_frame = int(start_time * fps)

    # 특정 구간의 시작 프레임과 종료 프레임을 계산
    special_start = start_frame
    special_end = start_frame + int(ending_range * fps)

    frame_count = 0
    while True:
        # 동영상에서 프레임을 읽음
        ret, frame = video.read()

        # 읽은 프레임이 없으면 종료
        if not ret:
            break

        # 특정 구간의 프레임인 경우 레이블을 1로, 그렇지 않은 경우 레이블을 0으로 설정
        label = 1 if special_start <= frame_count <= special_end else 0

        # 이미지 파일명을 생성
        img_filename = os.path.join(output_dir, filename_format.format(number=frame_count, label=label))

        # 이미지 파일 저장
        cv2.imwrite(img_filename, frame)

        frame_count += 1

    video.release()
    cv2.destroyAllWindows()

    print(f"{frame_count}개의 이미지가 저장되었습니다.")



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Save video frames with specific time range.')

    parser.add_argument('input_dir', type=str, help='Path to the input video dir.')
    parser.add_argument('output_dir', type=str, help='Directory to save the output images.')
    args = parser.parse_args()

    for filename in os.listdir(args.input_dir):
        if is_video_file(filename):
            output_format, start_time, ending_point = video_name_split_generater(filename)
            video_path = os.path.join(args.input_dir, filename)
            print(f"Processing video: {video_path}")
            output_format =  output_format + "_{number:04d}_label_{label}.png" # 저장할 이미지의 파일명 형식을 입력하세요
            save_video_frames(video_path, args.output_dir, output_format, start_time, ending_point)

