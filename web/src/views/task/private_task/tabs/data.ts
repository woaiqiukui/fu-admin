import { getPortInfo } from '../api';

/**
 * 端口信息
 */
interface PortInfo {
  key: number,
  ip: string,
  port: number,
  tag: string[],
}

export const portInfo: PortInfo[] = getPortInfo();
