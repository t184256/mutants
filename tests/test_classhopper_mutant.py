import mutants


class Duck:
    feathers = True

    def quack(self):
        return 'quack'


class Wolf:
    teeth = 'sharp'

    def quack(self):
        return 'no quack'


def test_classhopper_basic():
    def class_toggler(animal):
        return Wolf if isinstance(animal, Duck) else Duck

    tracy = mutants.ClassHopperMutant(Duck(), class_toggler)
    assert tracy.quack() == 'no quack'
    assert tracy.quack() == 'quack'
    assert tracy.teeth == 'sharp'
    tracy.name = 'Tracy'
    assert tracy.name == 'Tracy'

    def class_extender(animal):
        class SleepyAnimal(animal.__class__):
            def quack(self):
                return super().quack() + ' zzz'
        return SleepyAnimal

    zetta = mutants.ClassHopperMutant(Duck(), class_extender)
    assert zetta.quack() == 'quack zzz'
