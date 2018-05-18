from __future__ import print_function
import neat
import pickle
import visualize

def run(inputs, outputs, config_file):

    def eval_genomes(genomes, config):
        for _, genome in genomes:
            genome.fitness = len(outputs)
            net = neat.nn.FeedForwardNetwork.create(genome, config)
            for xi, xo in zip(inputs, outputs):
                output = net.activate(xi)
                genome.fitness -= (output[0] - xo[0]) ** 2
            genome.fitness = genome.fitness / len(outputs)

    # Load configuration.
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)

    # Create the population, which is the top-level object for a NEAT run.
    p = neat.Population(config)

    # Add a stdout reporter to show progress in the terminal.
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.StdOutReporter(True))

    # Run until a solution is found.
    winner, evol =  p.run(eval_genomes, 1000)

    # Display the winning genome.
    print('\nBest genome:\n{!s}'.format(winner))

    winner_net = neat.nn.FeedForwardNetwork.create(winner, config)

    visualize.plot_stats(stats, ylog=True, view=False, filename="feedforward-fitness-d.svg")
    visualize.plot_species(stats, view=False, filename="feedforward-speciation-d.svg")

    node_names = {-1: 'I1', -2: 'I2', -3: 'I3', -4: 'I4', -5: 'I5', -6: 'I6', -7: 'I7', -8: 'I8', 0: 'Output'}
    visualize.draw_net(config, winner, False, node_names=node_names)

    visualize.draw_net(config, winner, view=False, node_names=node_names,
                           filename="winner-feedforward-d.gv")
    visualize.draw_net(config, winner, view=False, node_names=node_names,
                           filename="winner-feedforward-enabled-d.gv", show_disabled=False)

    return {'net': winner_net, 'genome': winner, 'evol': evol}

# # Save the winner.
# with open('winner-feedforward', 'wb') as f:
#     pickle.dump(winner, f)

# # Show output of the most fit genome against training data.
# print('\nOutput:')
# winner_net = neat.nn.FeedForwardNetwork.create(winner, config)
# # for xi, xo in zip(xor_inputs, xor_outputs):
# #     output = winner_net.activate(xi)
# #     print("  input {!r}, expected output {!r}, got {!r}".format(xi, xo, output))


# visualize.draw_net(config, winner, view=True, node_names=node_names,
#                        filename="winner-feedforward-enabled-pruned-d.gv", show_disabled=False, prune_unused=True)