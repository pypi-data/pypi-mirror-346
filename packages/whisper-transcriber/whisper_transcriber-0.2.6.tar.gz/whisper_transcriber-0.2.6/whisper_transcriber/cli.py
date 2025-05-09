"""Command-line interface for Whisper Transcriber."""

import argparse
import sys
import os
from pathlib import Path
from .transcriber import WhisperTranscriber
from .utils import check_dependencies, validate_file_path


def validate_io_paths(input_path, output_path=None):
    """
    Validate input and output file paths.
    
    Args:
        input_path (str): Input file path
        output_path (str, optional): Output file path
        
    Returns:
        bool: True if valid, False otherwise
    """
    # Check if input file exists and is safe
    if not os.path.exists(input_path):
        print(f"Error: Input file '{input_path}' does not exist.")
        return False
        
    if not validate_file_path(input_path):
        print(f"Error: Input path '{input_path}' contains unsafe characters.")
        return False
        
    # Check output path
    if output_path and not validate_file_path(output_path):
        print(f"Error: Output path '{output_path}' contains unsafe characters.")
        return False
        
    # Check if we have write permissions for output
    if output_path:
        output_dir = os.path.dirname(output_path)
        if output_dir:
            try:
                if not os.path.exists(output_dir):
                    os.makedirs(output_dir, exist_ok=True)
                test_file = os.path.join(output_dir, ".write_test")
                with open(test_file, "w") as f:
                    f.write("")
                os.remove(test_file)
            except (PermissionError, OSError):
                print(f"Error: No write permission in output directory '{output_dir}'.")
                return False
                
    return True


def validate_model_name(model_name):
    """
    Validate model name for basic security checks.
    
    Args:
        model_name (str): Model name to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    # We still need to check for dangerous characters to prevent injection
    allowed_chars = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_./")
    
    # Check model name characters for security purposes only
    if not all(c in allowed_chars for c in model_name):
        print(f"Error: Invalid characters in model name '{model_name}'")
        return False
        
    # Allow any model format that passes the basic security check
    return True


def validate_numeric_args(args):
    """
    Validate numeric arguments.
    
    Args:
        args (Namespace): Parsed command-line arguments
        
    Returns:
        bool: True if valid, False otherwise
    """
    # Min segment should be positive and less than max segment
    if args.min_segment <= 0 or args.min_segment >= args.max_segment:
        print(f"Error: min-segment ({args.min_segment}) must be positive and less than max-segment ({args.max_segment})")
        return False
        
    # Silence duration should be positive
    if args.silence_duration <= 0:
        print(f"Error: silence-duration ({args.silence_duration}) must be positive")
        return False
        
    # Sample rate should be positive and reasonable
    valid_sample_rates = [8000, 16000, 22050, 24000, 32000, 44100, 48000]
    if args.sample_rate <= 0:
        print(f"Error: sample-rate ({args.sample_rate}) must be positive")
        return False
    elif args.sample_rate not in valid_sample_rates:
        print(f"Warning: Unusual sample rate: {args.sample_rate}. Common rates are: {valid_sample_rates}")
        
    # Batch size should be positive and reasonable
    if args.batch_size <= 0 or args.batch_size > 64:
        print(f"Error: batch-size ({args.batch_size}) must be between 1 and 64")
        return False
        
    # New parameter checks
    if args.temperature < 0 or args.temperature > 1.5:
        print(f"Error: temperature ({args.temperature}) must be between 0.0 and 1.5")
        return False
        
    if args.top_p is not None and (args.top_p <= 0 or args.top_p >= 1):
        print(f"Error: top_p ({args.top_p}) must be between 0 and 1")
        return False
        
    if args.beam_size < 1 or args.beam_size > 10:
        print(f"Error: beam_size ({args.beam_size}) must be between 1 and 10")
        return False
        
    if args.chunk_size < 10 or args.chunk_size > 3600:
        print(f"Error: chunk_size ({args.chunk_size}) must be between 10 and 3600 seconds")
        return False
        
    if args.parallel_jobs is not None and args.parallel_jobs < 1:
        print(f"Error: parallel_jobs ({args.parallel_jobs}) must be at least 1")
        return False
        
    return True


def main():
    """Command line interface for the whisper transcriber."""
    parser = argparse.ArgumentParser(description="Transcribe audio files using Whisper models")
    
    parser.add_argument("input", help="Input audio file or directory")
    parser.add_argument("-o", "--output", help="Output file path (optional)")
    parser.add_argument("-m", "--model", default="openai/whisper-small", 
                        help="Whisper model to use (default: openai/whisper-small)")
    parser.add_argument("--hf-token", help="HuggingFace API token")
    parser.add_argument("--min-segment", type=float, default=5, 
                        help="Minimum segment length in seconds (default: 5)")
    parser.add_argument("--max-segment", type=float, default=15, 
                        help="Maximum segment length in seconds (default: 15)")
    parser.add_argument("--silence-duration", type=float, default=0.2, 
                        help="Minimum silence duration in seconds (default: 0.2)")
    parser.add_argument("--sample-rate", type=int, default=16000, 
                        help="Audio sample rate (default: 16000)")
    parser.add_argument("--batch-size", type=int, default=8, 
                        help="Batch size for transcription (default: 8)")
    
    # Add new parameters for memory optimization and parallel processing
    parser.add_argument("--chunk-size", type=int, default=600,
                        help="Size of audio chunks in seconds for memory-efficient processing (default: 600)")
    parser.add_argument("--parallel-jobs", type=int, default=None,
                        help="Number of parallel jobs for silence detection (default: automatic)")
    parser.add_argument("--two-pass", action="store_true",
                        help="Use two-pass transcription for improved segment boundaries")
    
    # Add new parameters for generation control
    parser.add_argument("--temperature", type=float, default=0.0,
                        help="Temperature for sampling, higher values make output more random (default: 0.0)")
    parser.add_argument("--top-p", type=float, default=None,
                        help="Top-p sampling probability threshold (default: None)")
    parser.add_argument("--beam-size", type=int, default=5,
                        help="Beam size for beam search (default: 5)")
    
    # Add new parameter for beam search (as an alias for beam-size)
    parser.add_argument("--num-beams", type=int, default=None,
                        help="Alias for beam-size (number of beams for beam search)")
    
    # Existing parameters
    parser.add_argument("--normalize", action="store_true", 
                        help="Normalize audio volume")
    parser.add_argument("--no-text-normalize", action="store_true", 
                        help="Skip text normalization")
    parser.add_argument("--no-timestamps", action="store_true", 
                        help="Don't print timestamps during processing")
    parser.add_argument("--quiet", action="store_true",
                        help="Run in quiet mode (suppress transcript printing)")
    parser.add_argument("--json", action="store_true",
                        help="Output results as JSON instead of text")
    
    args = parser.parse_args()
    
    try:
        # Validate inputs
        if not validate_io_paths(args.input, args.output):
            sys.exit(1)
            
        if not validate_model_name(args.model):
            sys.exit(1)
            
        if not validate_numeric_args(args):
            sys.exit(1)
            
        # Check dependencies
        if not check_dependencies():
            print("Error: Missing required dependencies. Please install ffmpeg.")
            sys.exit(1)
        
        # Get HF token from environment if not provided
        if not args.hf_token and "HF_TOKEN" in os.environ:
            args.hf_token = os.environ["HF_TOKEN"]
        
        # Create and run transcriber
        try:
            transcriber = WhisperTranscriber(args.model, args.hf_token)
            
            # Determine verbosity - always set to False for JSON output
            verbose = not args.quiet and not args.json
            
            # Handle num_beams overriding beam_size if both are provided
            if args.num_beams is not None:
                beam_size = args.num_beams
            else:
                beam_size = args.beam_size
            
            results = transcriber.transcribe(
                args.input,
                output=args.output,
                min_segment=args.min_segment,
                max_segment=args.max_segment,
                silence_duration=args.silence_duration,
                sample_rate=args.sample_rate,
                batch_size=args.batch_size,
                normalize=args.normalize,
                normalize_text=not args.no_text_normalize,
                print_timestamps=not args.no_timestamps,
                verbose=verbose,
                two_pass=args.two_pass,
                chunk_size=args.chunk_size,
                parallel_jobs=args.parallel_jobs,
                temperature=args.temperature,
                top_p=args.top_p,
                beam_size=beam_size
            )
            
            # Handle JSON output if requested
            if args.json and results:
                import json
                # Convert the results to a serializable format
                serializable_results = []
                for segment in results:
                    serializable_results.append({
                        "start": segment["start"],
                        "end": segment["end"],
                        "transcript": segment["transcript"]
                    })
                print(json.dumps(serializable_results, ensure_ascii=False, indent=2))
            
        except Exception as e:
            print(f"Error during transcription: {str(e)}")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\nTranscription interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
