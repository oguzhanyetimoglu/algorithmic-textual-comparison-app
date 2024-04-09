export { TenK, TenKList };

declare global {
  interface TenK {}
  interface TenKList extends Array<TenK> {}
}
