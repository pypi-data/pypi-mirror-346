// Override for vfile type definitions
declare module 'vfile' {
  interface VFile {
    basename: string;
    stem: string;
    // Other properties and methods as needed
  }
  
  // Export constructor and other functions
  export function VFile(options?: any): VFile;
  export default VFile;
} 