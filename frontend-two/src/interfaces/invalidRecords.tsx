export type InvalidRecordRow = {
    [key: string]: string;
  };
  export type InvalidRecords = {
    [key: string]: InvalidRecordRow[];
  };


export type InvalidData = {
  records: InvalidRecords;
  description: string;
}