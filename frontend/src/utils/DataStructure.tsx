import { InvalidRecords } from "../interfaces/invalidRecords";

export const splitArray = (records: InvalidRecords, size = 5) => {
    const result: { [key: string]: InvalidRecords } = {};
    let count = 1;
    let index = 0;
    for (let i = 0; i < Object.keys(records).length; i++) {
      if (count === 1) {
        result[index] = {};
      }
      const recordkey = Object.keys(records)[i];
      result[index][recordkey] = records[recordkey];
      count++;
      if (count > size) {
        count = 1;
        index++;
      }
    }
    return result;
  };
