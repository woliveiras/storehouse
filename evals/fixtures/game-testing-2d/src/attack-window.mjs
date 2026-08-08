export class AttackWindow {
  constructor(){ this.seen=new Set(); this.paused=false }
  attack(id){ if(this.paused || this.seen.has(id)) return false; this.seen.add(id); return true }
  setPaused(value){ this.paused=value }
  restart(){ this.seen.clear(); this.paused=false }
}
