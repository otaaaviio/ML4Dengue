import os
import shutil
import random


def get_files_from_directory(directory):
    images = [file for file in os.listdir(directory) if file.endswith('.jpg')]

    prefix_names = [os.path.splitext(file)[0] for file in images]

    # Select only images with annotations
    selected = [name for name in prefix_names if os.path.exists(os.path.join(directory, name + '.xml'))]

    print(f'Found {len(selected)} images with annotations')

    return selected


def distribute_files(
        files,
        source_dir,
        train_directory,
        validate_directory,
        test_directory,
        train_ratio=0.7,
        validate_ratio=0.15):
    # shuffle the files to randomize the distribution
    random.seed(42)
    random.shuffle(files)

    # calculate the number of files for each split
    train_count = int(len(files) * train_ratio)
    validate_count = int(len(files) * validate_ratio)

    # distribute files to train, validate, and test folders
    for i, file in enumerate(files):
        if i < train_count:
            destination_dir = train_directory
        elif i < train_count + validate_count:
            destination_dir = validate_directory
        else:
            destination_dir = test_directory

        # Copy the jpg and xml file to the destination directory
        jpg = file + '.jpg'
        xml = file + '.xml'
        print(f'Copying {file} to {destination_dir}')
        shutil.copy(os.path.join(source_dir, jpg), os.path.join(destination_dir, jpg))
        shutil.copy(os.path.join(source_dir, xml), os.path.join(destination_dir, xml))


def main():
    # Define the source, train, validate, and test directories
    current_dir = os.path.dirname(os.path.abspath(__file__))
    source_dir = os.path.join(current_dir, 'all-images')
    train_directory = os.path.join(current_dir, 'result/train')
    validate_directory = os.path.join(current_dir, 'result/validate')
    test_directory = os.path.join(current_dir, 'result/test')

    files = get_files_from_directory(source_dir)
    distribute_files(files, source_dir, train_directory, validate_directory, test_directory)


if __name__ == "__main__":
    main()
