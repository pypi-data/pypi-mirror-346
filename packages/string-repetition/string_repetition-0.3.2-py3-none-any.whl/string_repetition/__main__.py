import argparse
import sys
import time
from .core import StringRepetitionDetector

def main():
    parser = argparse.ArgumentParser(description="检测字符串中的重复模式")
    parser.add_argument("text", nargs="?", help="要检测的文本")
    parser.add_argument("-f", "--file", help="从文件读取文本")
    parser.add_argument("-l", "--min-length", type=int, default=3, help="最小重复子串长度")
    parser.add_argument("-r", "--min-repeats", type=int, default=2, help="最小重复次数")
    parser.add_argument("-p", "--parallel", action="store_true", help="启用并行处理")
    
    args = parser.parse_args()
    
    # 创建检测器
    detector = StringRepetitionDetector(
        min_length=args.min_length,
        min_repeats=args.min_repeats
    )
    
    # 获取输入文本
    if args.file:
        try:
            with open(args.file, 'r', encoding='utf-8') as f:
                text = f.read()
        except Exception as e:
            print(f"读取文件错误: {e}", file=sys.stderr)
            return 1
    elif args.text:
        text = args.text
    else:
        # 如果没有提供文本，显示帮助
        parser.print_help()
        return 0
    
    # 执行检测并计时
    start_time = time.time()
    result = detector.detect_string(text, parallel=args.parallel)
    end_time = time.time()
    
    # 输出结果
    if result.has_repetition:
        print(f"找到重复子串: '{result.substring}'")
        print(f"重复次数: {result.repetition_count}")
        print(f"位置: {result.start_pos}-{result.end_pos}")
    else:
        print("未找到符合条件的重复子串")
    
    print(f"处理耗时: {(end_time - start_time)*1000:.2f}ms")
    return 0

if __name__ == "__main__":
    sys.exit(main())
