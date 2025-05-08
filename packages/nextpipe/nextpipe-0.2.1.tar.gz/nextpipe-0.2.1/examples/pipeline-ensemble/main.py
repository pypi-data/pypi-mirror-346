import nextmv

from nextpipe import FlowSpec, app, log, needs, repeat, step

# Define the options for the workflow
parameters = [
    nextmv.Parameter("instance", str, "latest", "App instance to use. Default is devint.", False),
]
options = nextmv.Options(*parameters)


# >>> Workflow definition
class Flow(FlowSpec):
    @app(
        app_id="routing-nextroute",
        instance_id=options.instance,
        parameters={"model.constraints.enable.cluster": True},
    )
    @repeat(repetitions=3)
    @step
    def run_nextroute():
        """Runs the model."""
        pass

    @needs(predecessors=[run_nextroute])
    @step
    def pick_best(results: list[dict]):
        """Aggregates the results."""
        log(f"Values: {[result['statistics']['result']['value'] for result in results]}")
        best_solution_idx = min(
            range(len(results)),
            key=lambda i: results[i]["statistics"]["result"]["value"],
        )
        return results[best_solution_idx]


def main():
    # Load input data
    input = nextmv.load()

    # Run workflow
    flow = Flow("DecisionFlow", input.data)
    flow.run()
    nextmv.write(flow.get_result(flow.pick_best))


if __name__ == "__main__":
    main()
