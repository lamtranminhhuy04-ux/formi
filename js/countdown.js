/* Pure date helpers; explicit timezone offsets avoid locale-dependent parsing. */
window.UniverseClock = (() => {
  function timestamp(value) {
    if (typeof value !== "string" || !/(Z|[+-]\d{2}:\d{2})$/.test(value)) return NaN;
    return Date.parse(value);
  }
  function parts(milliseconds) {
    const seconds = Math.floor(Math.max(0, Number.isFinite(milliseconds) ? milliseconds : 0) / 1000);
    return {days:Math.floor(seconds/86400),hours:Math.floor(seconds/3600)%24,minutes:Math.floor(seconds/60)%60,seconds:seconds%60};
  }
  function remaining(target, now = Date.now()) {
    const time = timestamp(target);
    return {valid:Number.isFinite(time),ended:Number.isFinite(time) && now >= time,...parts(time-now)};
  }
  function elapsed(start, now = Date.now()) {return parts(now-timestamp(start));}
  return {timestamp,parts,remaining,elapsed};
})();
