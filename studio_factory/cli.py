"""Offline creative factory CLI. No Higgsfield API or model generation."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
from .core import Factory, FactoryError
from .managers import manager

def parser():
    p=argparse.ArgumentParser(prog="studio-factory")
    p.add_argument("--db",default=".factory/registry.sqlite3")
    sub=p.add_subparsers(dest="cmd",required=True)
    a=sub.add_parser("init"); a.add_argument("project"); a.add_argument("--limit",type=int,default=9000)
    a=sub.add_parser("publish"); a.add_argument("domain"); a.add_argument("namespace"); a.add_argument("key"); a.add_argument("uri"); a.add_argument("payload_json"); a.add_argument("--previous",default=None)
    a=sub.add_parser("handoff"); a.add_argument("project"); a.add_argument("producer"); a.add_argument("consumer"); a.add_argument("asset_id"); a.add_argument("key"); a.add_argument("--evidence",required=True)
    a=sub.add_parser("ack"); a.add_argument("consumer"); a.add_argument("event_id")
    a=sub.add_parser("reference"); a.add_argument("consumer_id"); a.add_argument("source_id"); a.add_argument("--relation",default="uses")
    a=sub.add_parser("gate"); a.add_argument("project"); a.add_argument("gate"); a.add_argument("state",choices=["APPROVED","BLOCKED","NOT_RUN"]); a.add_argument("--approver",default=""); a.add_argument("--evidence",default="")
    a=sub.add_parser("check-generation"); a.add_argument("project"); a.add_argument("--estimated",type=int,required=True); a.add_argument("--spent",type=int,required=True); a.add_argument("--actor",required=True)
    a=sub.add_parser("manifest"); a.add_argument("project"); a.add_argument("--output")
    return p

def main(argv=None):
    p=parser(); opts=p.parse_args(argv); store=Factory(opts.db)
    try:
        if opts.cmd=="init":
            result={"project":store.create_project(opts.project,opts.limit)}
        elif opts.cmd=="publish":
            result={"asset_id":manager(opts.domain,store).publish(
                opts.namespace,opts.key,opts.uri,json.loads(opts.payload_json),
                expected_previous=opts.previous)}
        elif opts.cmd=="handoff":
            result={"event_id":manager(opts.producer,store).send(
                opts.project,opts.consumer,opts.asset_id,opts.key,json.loads(opts.evidence))}
        elif opts.cmd=="ack":
            manager(opts.consumer,store).receive(opts.event_id);result={"state":"ACK"}
        elif opts.cmd=="reference":
            store.reference(opts.consumer_id,opts.source_id,opts.relation);result={"state":"LINKED"}
        elif opts.cmd=="gate":
            store.set_gate(project=opts.project,gate=opts.gate,
                state=opts.state,approver=opts.approver,evidence_uri=opts.evidence)
            result={"state":opts.state}
        elif opts.cmd=="check-generation":
            result={"gate":store.require_generation_gate(
                opts.project,opts.estimated,opts.spent,opts.actor)}
        elif opts.cmd=="manifest":
            result=store.export_manifest(opts.project)
            if opts.output:
                Path(opts.output).write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
                result={"saved":opts.output,"count":len(result["artifacts"])}
        print(json.dumps(result,ensure_ascii=False,sort_keys=True,indent=2))
        return 0
    except (FactoryError,ValueError,json.JSONDecodeError) as exc:
        p.exit(2,f"BLOCKED: {exc}\n")
    finally:
        store.close()

if __name__=="__main__":
    raise SystemExit(main())
